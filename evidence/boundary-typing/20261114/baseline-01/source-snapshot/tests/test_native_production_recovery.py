"""Explicit package-transition checks; synthetic records are not native proof."""
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evaluations import native_production_recovery as recovery
from evaluations.host_trials import sha, write_json
from evaluations.native_trial_records import reference


class RuntimeRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'consumer'
        self.old = self.root / 'installed pixl'
        self.package = self.base / 'corrected-kit'
        self.previous, self.resumed = self.base / 'original', self.base / 'resumed'
        self.previous.mkdir()
        for name, content in {'runtime/pixl/plar_workflow.py': 'old',
                              'resources/pixl/plar_workflow.py': 'old',
                              'resources/spec/family-delivery.md': 'old spec',
                              'agents/pixl.md': 'same role', 'scripts/pixl.py': 'same bootstrap'}.items():
            path = self.old / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        self.manifest(self.old)
        shutil.copytree(self.old, self.package)
        (self.package / 'runtime/pixl/plar_workflow.py').write_text('corrected observer')
        (self.package / 'resources/pixl/plar_workflow.py').write_text('corrected observer')
        self.manifest(self.package)
        config = {'mcpServers': {'pixl-local': {'command': 'python', 'args': ['-B', str(self.old/'scripts/pixl.py'), 'mcp', '--root', str(self.root)]},
                                 'pixellab': {'type': 'http', 'url': 'https://api.pixellab.ai/mcp', 'headers': {'Authorization': 'Bearer ${PIXL_NATIVE_PROVIDER_TOKEN}'}}}}
        write_json(self.previous/'mcp.json', config)
        launch = {'host': 'claude', 'cwd': str(self.root),
                  'command': ['claude', '--session-id', 'parent', '--mcp-config', str(self.previous/'mcp.json'), '--plugin-dir', str(self.old)],
                  'configuration_files': {'package': str(self.old/'bundle-manifest.json'), 'claude_plugin_agent': str(self.old/'agents/pixl.md')}}
        write_json(self.previous/'launch.json', launch)
        self.prior = {'host': 'claude', 'session_id': 'parent', 'cwd': str(self.root), 'children': [{'id': 'child', 'role': 'pixl:pixl'}],
                      'calls': [], 'inputs': {'launch': reference(self.previous/'launch.json')},
                      'configuration': {'--mcp-config': reference(self.previous/'mcp.json'), 'package': reference(self.old/'bundle-manifest.json'),
                                        'file:claude_plugin_agent': reference(self.old/'agents/pixl.md')}}
        write_json(self.previous/'continuation.json', self.prior)

    def manifest(self, root):
        files = [{'path': p.relative_to(root).as_posix(), 'sha256': sha(p)} for p in sorted(root.rglob('*'))
                 if p.is_file() and p.name != 'bundle-manifest.json']
        write_json(root/'bundle-manifest.json', {'files': files})

    def fake_prepare(self, previous, destination, prompt, child):
        destination.mkdir()
        launch = recovery.read(previous/'launch.json')
        launch['command'] = [launch['command'][0], *launch['command'][3:], '--resume', 'parent']
        launch.update(predecessor=reference(previous/'continuation.json'), continuation_mode='native_same_session', expected_session_id='parent', expected_child_id=child)
        write_json(destination/'launch.json', launch)
        write_json(destination/'identity.json', {'predecessor': reference(previous/'continuation.json'), 'original_consumer': str(self.root),
                                                'session_id': 'parent', 'child_id': child, 'mode': 'native_same_session'})
        (destination/'prompt.txt').write_text(prompt)

    def prepare(self, **kwargs):
        with patch.object(recovery, 'prepare_resume', side_effect=self.fake_prepare):
            return recovery.prepare(self.previous, self.resumed, 'No paid work; recover current handoff.', 'child', self.package, **kwargs)

    def test_transition_preserves_original_and_provider_configuration(self):
        original = recovery.inventory(self.old)
        self.prepare()
        receipt = recovery.verify_transition(self.previous, self.resumed)
        self.assertEqual(original, recovery.inventory(self.old))
        self.assertEqual(['bundle-manifest.json', 'resources/pixl/plar_workflow.py', 'runtime/pixl/plar_workflow.py'], receipt['changed'])
        self.assertEqual(recovery.read(self.previous/'mcp.json')['mcpServers']['pixellab'],
                         recovery.read(self.resumed/'mcp.json')['mcpServers']['pixellab'])

    def test_unreviewed_profile_change_cannot_prepare(self):
        (self.package/'agents/pixl.md').write_text('different authority')
        self.manifest(self.package)
        with self.assertRaisesRegex(ValueError, 'unreviewed package'):
            self.prepare()
        self.assertFalse(self.resumed.exists())

    def test_runtime_and_source_copy_must_agree(self):
        (self.package/'resources/pixl/plar_workflow.py').write_text('different implementation')
        self.manifest(self.package)
        with self.assertRaisesRegex(ValueError, 'copies disagree'):
            self.prepare()

    def test_recovery_does_not_accept_rewritten_provider_config(self):
        self.prepare()
        config = recovery.read(self.resumed/'mcp.json')
        config['mcpServers']['pixellab']['url'] = 'https://example.invalid'
        write_json(self.resumed/'mcp.json', config)
        with self.assertRaisesRegex(ValueError, 'more than the declared'):
            recovery.verify_transition(self.previous, self.resumed)

    def test_original_frozen_package_still_must_verify(self):
        self.prepare()
        (self.old/'runtime/pixl/plar_workflow.py').write_text('silently replaced')
        with self.assertRaisesRegex(ValueError, 'Frozen package payload changed'):
            recovery.verify_transition(self.previous, self.resumed)

    def test_actual_continuation_rejects_changed_child(self):
        receipt = self.prepare()
        config = dict(self.prior['configuration'])
        kit = Path(receipt['new_kit']['root'])
        config.update({'--mcp-config': reference(self.resumed/'mcp.json'), 'package': reference(kit/'bundle-manifest.json'),
                       'file:claude_plugin_agent': reference(kit/'agents/pixl.md')})
        current = {**self.prior, 'mode': 'native_same_session', 'expected_session_id': 'parent', 'expected_child_id': 'child',
                   'observed_expected_session': True, 'predecessor': reference(self.previous/'continuation.json'), 'configuration': config,
                   'inputs': {name: reference(self.resumed/name) for name in ('launch.json','identity.json','prompt.txt')}}
        write_json(self.resumed/'continuation.json', current)
        combined, proof = recovery.verify_continuation(self.previous, self.resumed, 'child')
        self.assertEqual('parent', combined['session_id'])
        self.assertIn('runtime upgrade', proof['scope'])
        current['expected_child_id'] = 'replacement'
        write_json(self.resumed/'continuation.json', current)
        with self.assertRaisesRegex(ValueError, 'native parent, child'):
            recovery.verify_continuation(self.previous, self.resumed, 'child')

    def test_intermediate_report_archive_is_bound_independently_of_live_report(self):
        middle = self.base/'intermediate'
        self.fake_prepare(self.previous, middle, 'Continue original work.', 'child')
        report = self.root/recovery.WORK/'REPORT.json'
        report.parent.mkdir(parents=True)
        report.write_text('incomplete first report')
        (middle/'outputs').mkdir()
        shutil.copyfile(report, middle/'outputs/REPORT.json')
        (middle/'stdout.jsonl').write_text('{}\n')
        current = {**self.prior, 'mode': 'native_same_session', 'status': 'finished',
                   'expected_session_id': 'parent', 'expected_child_id': 'child', 'observed_expected_session': True,
                   'predecessor': reference(self.previous/'continuation.json'), 'artifacts': [reference(report)],
                   'inputs': {name: reference(middle/name) for name in ('launch.json','identity.json','prompt.txt')}}
        write_json(middle/'continuation.json', current)
        self.prepare(intermediate=(middle,))
        report.write_text('new current report; earlier version remains retained')
        self.assertEqual(1, len(recovery.verify_transition(self.previous,self.resumed)['intermediate_attempts']))
        (middle/'outputs/REPORT.json').write_text('rewritten historical evidence')
        with self.assertRaisesRegex(ValueError, 'archive is incomplete'):
            recovery.verify_transition(self.previous,self.resumed)


if __name__ == '__main__':
    unittest.main()
