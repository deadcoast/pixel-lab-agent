"""Real loopback faults for CF-08; no upstream provider or native-model claims."""
import base64
import http.client
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.request import urlopen

from evaluations.provider_recovery_fixture import (
    RecoveryProvider,
    digest,
    handle,
    start_download_server,
)

ROOT = Path(__file__).resolve().parents[1]
NEGATIVE = ROOT / 'evidence/host-evaluation/fixture-inputs/candidate.png'
POSITIVE = ROOT / 'evidence/host-evaluation/fixture-inputs/reference.png'


class ProviderRecoveryFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.provider = RecoveryProvider(self.folder, NEGATIVE, POSITIVE)
        self.arguments = {'method': 'reference', 'description': 'Original controlled recovery request',
                          'image_base64': base64.b64encode(NEGATIVE.read_bytes()).decode(),
                          'reference_image': {'base64': base64.b64encode(POSITIVE.read_bytes()).decode()}}

    def accepted(self):
        value, error, image = self.provider.call('edit_image_pro_flash', self.arguments)
        self.assertTrue(error)
        self.assertNotIn('job_id', value)
        self.assertIsNone(image)
        return 'controlled-recovery-0001'

    def test_lost_response_keeps_exact_match_and_refuses_second_submission(self):
        ident = self.accepted()
        cold = RecoveryProvider(self.folder, NEGATIVE, POSITIVE)
        result, _, _ = cold.call('list_jobs', {'include_recent': True})
        self.assertEqual(result['jobs'][0]['job_id'], ident)
        self.assertEqual(result['jobs'][0]['arguments'], self.arguments)
        self.assertEqual(cold.state['accepted_submissions'], 1)
        with self.assertRaisesRegex(ValueError, 'recover it'):
            cold.call('edit_image_pro_flash', self.arguments)
        self.assertEqual(len(cold.state['jobs']), 1)

    def test_progression_is_persistent_and_never_supplies_inline_image(self):
        ident = self.accepted()
        response, _, image = self.provider.call('get_image', {'job_id': ident})
        self.assertEqual(response['status'], 'processing')
        self.assertNotIn('images', response)
        self.assertIsNone(image)
        cold = RecoveryProvider(self.folder, NEGATIVE, POSITIVE)
        cold.base_url = 'http://127.0.0.1:12345'
        response = handle(cold, {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
                                'params': {'name': 'get_image', 'arguments': {'job_id': ident}}})
        result = response['result']
        self.assertEqual(result['structuredContent']['status'], 'completed')
        self.assertTrue(all(block['type'] == 'text' for block in result['content']))
        self.assertEqual(result['structuredContent']['images'][0]['sha256'], digest(POSITIVE.read_bytes()))
        with self.assertRaises(ValueError):
            cold.call('get_image', {'job_id': 'absent-does-not-prove-non-acceptance'})

    def test_real_short_http_body_then_new_connection_recovers_same_resource(self):
        ident = self.accepted()
        self.provider.call('get_image', {'job_id': ident})
        self.provider.call('get_image', {'job_id': ident})
        first = start_download_server(self.provider)
        try:
            with urlopen(self.provider.base_url + '/' + ident + '.png', timeout=5) as response:
                self.assertEqual(int(response.headers['Content-Length']), len(POSITIVE.read_bytes()))
                with self.assertRaises(http.client.IncompleteRead) as error:
                    response.read()
            partial = error.exception.partial
            self.assertTrue(partial)
            self.assertNotEqual(partial, POSITIVE.read_bytes())
        finally:
            first.shutdown()
            first.server_close()
        cold = RecoveryProvider(self.folder, NEGATIVE, POSITIVE)
        second = start_download_server(cold)
        try:
            observation, _, _ = cold.call('get_image', {'job_id': ident})
            with urlopen(observation['images'][0]['download_url'], timeout=5) as response:
                self.assertEqual(response.read(), POSITIVE.read_bytes())
        finally:
            second.shutdown()
            second.server_close()
        state = json.loads((self.folder / 'provider-state.json').read_bytes())
        self.assertEqual(state['accepted_submissions'], 1)
        self.assertEqual(state['jobs'][0]['download_attempts'], 2)
        events = [json.loads(line) for line in (self.folder / 'provider-calls.jsonl').read_text().splitlines()]
        served = [event['download'] for event in events if 'download' in event]
        self.assertEqual([True, False], [row['interrupted'] for row in served])
        self.assertEqual(served[0]['served_sha256'], digest(partial))
        self.assertEqual(served[1]['served_sha256'], digest(POSITIVE.read_bytes()))

    def test_stdio_processes_observe_one_shared_job_and_fresh_url(self):
        ident = self.accepted()
        observations = []
        for _ in range(2):
            request = {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
                       'params': {'name': 'get_image', 'arguments': {'job_id': ident}}}
            process = subprocess.run([sys.executable, '-B', '-m', 'evaluations.provider_recovery_fixture',
                                      '--folder', str(self.folder), '--negative', str(NEGATIVE),
                                      '--positive', str(POSITIVE)], cwd=ROOT,
                                     input=json.dumps(request) + '\n', capture_output=True, text=True, timeout=20, check=False)
            self.assertEqual(process.returncode, 0, process.stderr)
            observations.append(json.loads(process.stdout)['result']['structuredContent'])
        self.assertEqual(['processing', 'completed'], [row['status'] for row in observations])
        self.assertTrue(observations[1]['images'][0]['download_url'].startswith('http://127.0.0.1:'))


if __name__ == '__main__':
    unittest.main()
