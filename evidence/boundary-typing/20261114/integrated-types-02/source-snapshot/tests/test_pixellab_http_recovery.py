"""Interrupted local retrieval recovery from an already retained HTTP response."""

import hashlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PIL import Image

from evaluations.pixellab_mock import MockTransport
from pixl import codec, jobs, store
from pixl.pixellab_http import Workflow
from tests.lifecycle_support import sample


class HTTPRetrievalRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.folder = self.root / '.pixl'
        doc = sample(self.root)
        doc.records['choice'].fields['vl'] = [32, 32]
        doc.records['contract'].fields['px'] = [32, 32]
        store.initialize(self.folder, doc, self.root)
        self.image = self.root / 'fixture.png'
        Image.new('RGBA', (32, 32), 'teal').save(self.image)
        self.data = self.image.read_bytes()
        self.digest = hashlib.sha256(self.data).hexdigest()
        self.target = self.folder / 'downloads' / (self.digest + '.png')
        self.transport = MockTransport(self.image)
        self.workflow = Workflow(self.root, self.transport)
        self.guard = patch('socket.socket', side_effect=AssertionError('Unexpected real network call'))
        self.guard.start()
        self.addCleanup(self.guard.stop)
        self.workflow.prepare(
            '.pixl', self.expected(), 'job', 'task', 'output',
            {'description': 'Local retrieval fixture', 'image_size': {'width': 32, 'height': 32}, 'no_background': True},
            {'scope': 'Controlled transport only', 'evidence': {'fixture': True}},
        )
        self.workflow.submit('.pixl', self.expected(), 'job')
        self.workflow.poll('.pixl', self.expected(), 'job')
        self.workflow.poll('.pixl', self.expected(), 'job')
        self.calls = list(self.transport.calls)

    def expected(self):
        return codec.digest(store.load(self.folder))

    def import_image(self, expected=None):
        return Workflow(self.root, self.transport).import_image(
            '.pixl', self.expected() if expected is None else expected, 'job', 'output', 'candidate',
        )

    def files(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob('*') if p.is_file()}

    def test_partial_cache_is_preserved_and_recovered_without_another_provider_call(self):
        self.target.parent.mkdir()
        partial = self.data[:17]
        self.target.write_bytes(partial)
        result = self.import_image()
        download = result['download']
        self.assertEqual(self.target.read_bytes(), partial)
        self.assertNotEqual(download['path'], self.target.relative_to(self.root).as_posix())
        self.assertEqual((self.root / download['path']).read_bytes(), self.data)
        self.assertEqual(download['recovered_from'], {
            'path': self.target.relative_to(self.root).as_posix(),
            'sha256': hashlib.sha256(partial).hexdigest(), 'bytes': len(partial),
        })
        self.assertEqual(download['sha256'], self.digest)
        self.assertFalse(download['reused_download'])
        self.assertEqual(self.transport.calls, self.calls)
        candidate = store.load(self.folder).records['candidate']
        self.assertEqual((self.root / candidate.fields['ur']).read_bytes(), self.data)

    def test_interruption_before_atomic_replace_leaves_no_partial_download(self):
        before = self.expected()
        original = store.os.replace

        def interrupted(source, destination):
            if Path(destination) == self.target:
                raise OSError('controlled interruption before download publication')
            return original(source, destination)

        with patch('pixl.store.os.replace', side_effect=interrupted), self.assertRaises(OSError):
            self.import_image()
        self.assertFalse(self.target.exists())
        self.assertEqual(list(self.folder.rglob('.pixl-write-*')), [])
        self.assertEqual(self.expected(), before)
        result = self.import_image()
        self.assertEqual(self.target.read_bytes(), self.data)
        self.assertIsNone(result['download']['recovered_from'])
        self.assertEqual(self.transport.calls, self.calls)

    def test_interruption_between_download_and_import_reuses_complete_retained_bytes(self):
        before = self.expected()
        with patch('pixl.pixellab_http.jobs.import_artifact', side_effect=OSError('controlled interruption')), self.assertRaises(OSError):
            self.import_image()
        self.assertEqual(self.target.read_bytes(), self.data)
        self.assertEqual(self.expected(), before)
        self.assertNotIn('candidate', store.load(self.folder).records)
        result = self.import_image()
        self.assertTrue(result['download']['reused_download'])
        self.assertFalse(result['reused_import'])
        self.assertEqual(self.transport.calls, self.calls)

    def test_lost_successful_import_reply_reuses_current_candidate_and_all_bytes(self):
        publish = jobs._save

        def lost_reply(*args, **kwargs):
            publish(*args, **kwargs)
            raise OSError('controlled lost response after publication')

        with patch('pixl.jobs._save', side_effect=lost_reply), self.assertRaises(OSError):
            self.import_image()
        before = self.files()
        result = self.import_image()
        self.assertTrue(result['reused_import'])
        self.assertTrue(result['download']['reused_download'])
        self.assertEqual(self.files(), before)
        self.assertEqual(self.transport.calls, self.calls)
        self.assertEqual(len([e for e in result['job']['events'] if e['event'] == 'imported']), 1)

    def test_changed_recovery_cache_is_never_silently_repaired_or_imported(self):
        self.target.parent.mkdir()
        damaged = b'partial'
        self.target.write_bytes(damaged)
        recovered = self.target.parent / 'recovery' / (
            self.digest + '-from-' + hashlib.sha256(damaged).hexdigest() + '.png'
        )
        recovered.parent.mkdir()
        recovered.write_bytes(b'another conflicting file')
        before = self.files()
        with self.assertRaisesRegex(codec.PixlError, 'Retained recovery download changed'):
            self.import_image()
        self.assertEqual(self.files(), before)
        self.assertEqual(self.transport.calls, self.calls)

    def test_stale_import_does_not_materialize_or_repair_any_download(self):
        self.target.parent.mkdir()
        self.target.write_bytes(b'partial')
        before = self.files()
        with self.assertRaisesRegex(codec.PixlError, 'stale_write'):
            self.import_image(expected='0' * 64)
        self.assertEqual(self.files(), before)
        self.assertEqual(self.transport.calls, self.calls)


if __name__ == '__main__':
    unittest.main()
