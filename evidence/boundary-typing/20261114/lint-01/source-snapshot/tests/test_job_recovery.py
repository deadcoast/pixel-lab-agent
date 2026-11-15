"""Useful cold job recovery; all provider observations are controlled fixtures."""

import hashlib
import json
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from pixl import codec, jobs, service, store
from tests.lifecycle_support import sample


class JobRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.folder = self.root / '.pixl'
        doc = sample(self.root)
        second = deepcopy(doc.records['output'])
        second.id = 'second'
        doc.records['second'] = second
        doc.records['task'].fields['op'].append(codec.Ref('second'))
        store.initialize(self.folder, doc, self.root)
        self.source = self.root / 'download.png'
        Image.new('RGBA', (2, 2), 'teal').save(self.source)
        self.evidence = {'fixture': True, 'download': 'observed controlled bytes'}

    def expected(self):
        return codec.digest(store.load(self.folder))

    def files(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob('*') if p.is_file()}

    def prepare(self, job_id='job'):
        return jobs.prepare(
            self.folder, self.expected(), job_id, 'task', ['output', 'second'],
            'controlled-origin', 'fixture_image', {}, {'type': 'object'},
            {'source': 'controlled fixture declaration',
             'observed_at': '2026-09-11T12:00:00+00:00', 'evidence': {'fixture': True}},
            {'scope': 'local recovery check; no remote execution', 'evidence': {'fixture': True}},
            self.root,
        )

    def complete(self, job_id='job'):
        self.prepare(job_id)
        jobs.dispatch(self.folder, self.expected(), job_id, self.root)
        return jobs.observe(self.folder, self.expected(), job_id, 'succeeded',
                            self.evidence, 'fixture-' + job_id, self.root)

    def import_one(self, candidate='candidate', output='output', **changes):
        args = {'folder': self.folder, 'expected': self.expected(), 'job_id': 'job',
                'output_id': output, 'candidate_id': candidate, 'path': 'download.png',
                'evidence': self.evidence, 'root': self.root}
        args.update(changes)
        return jobs.import_artifact(**args)

    def test_unknown_report_retains_origin_uncertainty_and_no_dispatch_grant(self):
        self.prepare()
        jobs.dispatch(self.folder, self.expected(), 'job', self.root)
        before = self.files()
        row = service.job_report(self.folder / 'state.px', self.root)['jobs'][0]
        self.assertEqual(row['next_action'], 'reconcile')
        self.assertEqual(row['recovery']['action'], 'reconcile')
        self.assertEqual(row['recovery']['provider'], 'controlled-origin')
        self.assertIsNone(row['recovery']['remote_id'])
        self.assertEqual(row['recovery']['missing_outputs'], ['output', 'second'])
        self.assertNotIn('dispatch_request', row)
        self.assertEqual(self.files(), before)

    def test_known_job_then_partial_and_complete_imports_expose_usable_paths(self):
        self.prepare()
        jobs.dispatch(self.folder, self.expected(), 'job', self.root)
        running = jobs.observe(self.folder, self.expected(), 'job', 'running',
                               self.evidence, 'fixture-job', self.root)
        self.assertEqual(running['job']['recovery']['action'], 'observe')
        self.assertEqual(running['job']['recovery']['remote_id'], 'fixture-job')
        completed = jobs.observe(self.folder, self.expected(), 'job', 'succeeded',
                                 self.evidence, root=self.root)
        self.assertEqual(completed['job']['next_action'], 'retrieve_outputs')
        first = self.import_one()
        self.assertFalse(first['reused_import'])
        self.assertEqual(first['job']['recovery']['missing_outputs'], ['second'])
        self.assertEqual(first['job']['next_action'], 'retrieve_outputs')
        final = self.import_one('second-candidate', 'second')
        self.assertEqual(final['job']['next_action'], 'inspect_candidates')
        self.assertEqual(final['job']['recovery']['missing_outputs'], [])
        for item in final['job']['recovery']['imported']:
            self.assertEqual((self.root / item['path']).read_bytes(), self.source.read_bytes())
            self.assertEqual(item['sha256'], hashlib.sha256(self.source.read_bytes()).hexdigest())
            self.assertEqual(item['record_sha256'], codec.record_hash(store.load(self.folder).records[item['candidate_id']]))
        doc = store.load(self.folder)
        self.assertEqual(doc.records['task'].fields['ca'], [])
        self.assertEqual(doc.records['task'].fields['vr'], [])
        self.assertEqual(doc.records['task'].fields['st'], codec.Symbol('open'))

    def test_exact_import_replay_reuses_candidate_with_relocated_equal_bytes(self):
        self.complete()
        first = self.import_one()
        other = self.root / 'relocated.png'
        other.write_bytes(self.source.read_bytes())
        before = self.files()
        repeated = self.import_one(path=other.name)
        self.assertTrue(repeated['reused_import'])
        self.assertEqual(repeated['hash'], first['hash'])
        self.assertEqual(repeated['revision'], first['revision'])
        self.assertEqual(self.files(), before)
        self.assertEqual(len([e for e in repeated['job']['events'] if e['event'] == 'imported']), 1)

    def test_stale_expected_hash_cannot_replay_even_identical_import(self):
        self.complete()
        before_import = self.expected()
        self.import_one()
        before = self.files()
        with self.assertRaisesRegex(codec.PixlError, 'stale_write'):
            self.import_one(expected=before_import)
        self.assertEqual(self.files(), before)

    def test_changed_evidence_bytes_or_output_cannot_reuse_candidate_id(self):
        self.complete()
        self.import_one()
        altered = self.root / 'altered.png'
        Image.new('RGBA', (2, 2), 'red').save(altered)
        before = self.files()
        for changes in (
            {'evidence': {**self.evidence, 'fixture': 1}},
            {'evidence': {'fixture': True}},
            {'path': altered.name},
            {'output_id': 'second'},
        ):
            with self.subTest(changes=changes), self.assertRaisesRegex(codec.PixlError, 'job_artifact'):
                self.import_one(**changes)
            self.assertEqual(self.files(), before)

    def test_same_bytes_from_other_job_are_not_a_replayed_association(self):
        self.complete()
        self.import_one()
        self.complete('another')
        before = self.files()
        with self.assertRaisesRegex(codec.PixlError, 'job_artifact'):
            self.import_one(job_id='another')
        self.assertEqual(self.files(), before)

    def test_changed_output_context_blocks_replay_without_rewriting_old_import(self):
        self.complete()
        self.import_one()
        doc = store.load(self.folder)
        old_hash = codec.digest(doc)
        doc.records['q.visual'].fields['ck'] = 'A new fixture requirement.'
        doc.revision += 1
        store.commit(self.folder, doc, old_hash, self.root)
        before = self.files()
        with self.assertRaisesRegex(codec.PixlError, 'job_stale'):
            self.import_one()
        self.assertEqual(self.files(), before)

    def test_cli_cold_report_exposes_recovery_without_publishing(self):
        self.complete()
        before = self.files()
        result = subprocess.run(
            [sys.executable, '-m', 'pixl', 'jobs', str(self.folder / 'state.px'), '--root', str(self.root)],
            capture_output=True, text=True, check=False, timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        value = json.loads(result.stdout)
        self.assertEqual(value['jobs'][0]['recovery']['action'], 'retrieve_outputs')
        self.assertFalse(value['remote_executed'])
        self.assertEqual(self.files(), before)


if __name__ == '__main__':
    unittest.main()
