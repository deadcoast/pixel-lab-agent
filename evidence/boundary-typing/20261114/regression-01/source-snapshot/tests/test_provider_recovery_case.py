"""CF-08 preparation/retention boundaries; native behavior is graded separately."""
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from evaluations import provider_recovery_case as case
from evaluations.host_trials import inventory, sha, write_json
from pixl import codec, jobs, store


class ProviderRecoveryCaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'consumer'
        self.attempt = self.base / 'phase1'
        self.python = Path(sys.executable).resolve()

    def fake_readiness(self, destination, host, setup, python, **kwargs):
        """Only host launcher sampling is mocked; durable state/fixture/retention are real."""
        destination.mkdir()
        self.root.mkdir()
        kit = self.root / case.KIT
        kit.mkdir()
        (kit / 'payload.txt').write_text('controlled minimal package for case mechanics')
        write_json(kit / 'bundle-manifest.json', {'files': [{'path': 'payload.txt', 'sha256': sha(kit / 'payload.txt')}]})
        (self.root / 'BRIEF.md').write_text('Preserved earlier readiness context')
        role = self.root / 'role.toml'
        role.write_text('controlled role configuration, no native qualification')
        command = ['codex', 'exec', '-'] if host == 'codex' else ['claude', '--session-id', 'old-session', '--allowedTools', 'Read']
        configuration = {'package': str(kit / 'bundle-manifest.json'), 'role': str(role)}
        if host == 'claude':
            write_json(destination / 'mcp.json', {'mcpServers': {'pixl-local': {'command': str(python)}}})
            command += ['--mcp-config', str(destination / 'mcp.json')]
        write_json(destination / 'launch.json', {'host': host, 'cwd': str(self.root), 'command': command,
                                               'configuration_files': configuration})
        write_json(destination / 'identity.json', {'inputs': inventory(self.root), 'package_files': inventory(kit)})
        (destination / 'runner.py.txt').write_text('mocked native launcher setup only')
        return self.root

    def prepared(self, host='codex'):
        with patch.object(case.readiness_case, 'prepare', side_effect=self.fake_readiness):
            return case.prepare(self.attempt, host, self.python)

    def test_prepares_two_unknowns_one_original_acceptance_and_bound_source(self):
        self.prepared()
        case.verify_ready(self.attempt)
        doc = store.load(self.root / case.STORE)
        report = jobs.report(doc, self.root)
        self.assertEqual({'unknown'}, {row['state'] for row in report['jobs']})
        self.assertEqual({'recoverable-job', 'unresolved-job'}, {row['id'] for row in report['jobs']})
        self.assertTrue(all(not row['remote_id'] for row in report['jobs']))
        state = json.loads((self.attempt / 'provider/provider-state.json').read_bytes())
        self.assertEqual(state['accepted_submissions'], 1)
        self.assertEqual(len(state['jobs']), 1)
        self.assertIn('assets/robot.png', (self.root / 'src/avatar.ts').read_text())
        self.assertIn('one edit', (self.root / 'OWNER.md').read_text())
        self.assertIn('supersedes only OWNER.md', (self.root / case.AUTHORITY).read_text())
        self.assertNotIn(case.CANDIDATE, doc.records)
        self.assertFalse((self.root / 'assets/robot.png').exists())
        self.assertEqual(doc.records['source'].fields['dg'], sha(self.root / case.AUTHORITY))
        with zipfile.ZipFile(self.attempt / 'input-state.zip') as archive:
            self.assertIn(case.STORE + '/state.px', archive.namelist())

    def test_phase_retention_captures_state_journals_failed_bytes_and_refuses_overwrite(self):
        self.prepared()
        partial = self.root / case.WORK / 'phase-1/download.part'
        partial.write_bytes(b'actual controlled partial response')
        case.retain(self.attempt)
        receipt = json.loads((self.attempt / 'preservation.json').read_bytes())
        self.assertEqual(receipt['unexpected'], [])
        self.assertEqual(receipt['final_state']['canonical_hash'], codec.digest(store.load(self.root / case.STORE)))
        self.assertEqual((self.attempt / 'outputs/download.part').read_bytes(), partial.read_bytes())
        self.assertTrue((self.attempt / 'snapshots/final-jobs.json').is_file())
        self.assertTrue((self.attempt / 'provider-calls.jsonl').is_file())
        with self.assertRaisesRegex(ValueError, 'once'):
            case.retain(self.attempt)

    def test_cold_rounds_keep_exact_root_kit_provider_but_fresh_claude_identity(self):
        self.prepared('claude')
        case.retain(self.attempt)
        second = self.base / 'phase2'
        case.prepare_cold(self.attempt, second, self.python)
        old = json.loads((self.attempt / 'launch.json').read_bytes())
        new = json.loads((second / 'launch.json').read_bytes())
        self.assertEqual(old['cwd'], new['cwd'])
        self.assertEqual(old['configuration_files'], new['configuration_files'])
        self.assertNotEqual(old['command'][old['command'].index('--session-id') + 1],
                            new['command'][new['command'].index('--session-id') + 1])
        self.assertNotIn('--resume', new['command'])
        self.assertEqual(new['continuation_mode'], 'artifact_based_restart')
        case.retain(second)
        third = self.base / 'phase3'
        case.prepare_cold(second, third, self.python)
        identity = json.loads((third / 'identity.json').read_bytes())
        self.assertEqual(identity['authorized_changes'], [])
        case.retain(third)
        with self.assertRaisesRegex(ValueError, 'three-phase'):
            case.prepare_cold(third, self.base / 'phase4', self.python)

    def test_cold_refuses_changed_consumer_or_configuration(self):
        self.prepared()
        case.retain(self.attempt)
        source = self.root / 'src/avatar.ts'
        original = source.read_bytes()
        source.write_text('changed mapping')
        with self.assertRaisesRegex(ValueError, 'consumer changed'):
            case.prepare_cold(self.attempt, self.base / 'phase2', self.python)
        source.write_bytes(original)
        fixture = self.attempt / 'provider/provider_recovery_fixture.py'
        fixture.write_text('changed fixture')
        with self.assertRaisesRegex(ValueError, 'configuration changed'):
            case.prepare_cold(self.attempt, self.base / 'phase2', self.python)

    def test_retention_rejects_partial_name_prefix_as_delivered_asset(self):
        self.prepared()
        (self.root / 'assets/robot.png.bypass').write_bytes(b'not assigned')
        case.retain(self.attempt)
        receipt = json.loads((self.attempt / 'preservation.json').read_bytes())
        self.assertIn('assets/robot.png.bypass', receipt['unexpected'])

    def test_cold_codex_is_new_exec_and_previous_state_identity_is_final_snapshot(self):
        self.prepared()
        case.retain(self.attempt)
        second = self.base / 'phase2'
        case.prepare_cold(self.attempt, second, self.python)
        launch = json.loads((second / 'launch.json').read_bytes())
        self.assertNotIn('resume', launch['command'])
        identity = json.loads((second / 'identity.json').read_bytes())
        self.assertEqual(identity['predecessor']['state']['path'], str(self.attempt / 'snapshots/final-state.px'))
        self.assertEqual(launch['configuration_files']['provider_fixture'], str(self.attempt / 'provider/provider_recovery_fixture.py'))

    def test_prelaunch_refuses_provider_state_drift(self):
        self.prepared()
        provider = self.attempt / 'provider/provider-state.json'
        state = json.loads(provider.read_bytes())
        state['accepted_submissions'] = 2
        write_json(provider, state)
        with self.assertRaisesRegex(ValueError, 'provider state changed'):
            case.verify_ready(self.attempt)


if __name__ == '__main__':
    unittest.main()
