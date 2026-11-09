"""An accepted member is delivered only at its destination and with its family."""

import copy
import json
import shutil
import unittest
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from pixl import codec, completion, delivery, plar, store
from pixl.codec import Record, Ref, Symbol
from tests.family_support import family
from tests.lifecycle_support import add_verdict
from tests.test_plar_prepare import seed


class PLARFamilyDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'consumer'
        seed(self.root)
        self.folder = self.root / '.pixl/family'
        family(self.root, self.folder)
        queue = json.loads((self.root / 'plar.txt').read_bytes())
        asset = next(a for a in queue['assets'] if a['id'] == 'queue.working')
        asset['production'] = {'store': '.pixl/family', 'task': 'member.task', 'output': 'member.output'}
        asset['delivery']['path'] = 'assets/delivered.png'
        plar.save(self.root, queue, plar.read(self.root)['hash'])
        selected = plar.read(self.root, asset_id='queue.working', include_production=False)
        snapshot = self.root / 'selection.json'
        snapshot.write_text(json.dumps(selected), encoding='utf-8')
        document = store.load(self.folder)
        expected = codec.digest(document)
        document.records['selection'] = Record('selection', 'X', {'nm': 'Current synthetic selection', 'ur': 'selection.json', 'dg': sha256(snapshot.read_bytes()).hexdigest(), 'kd': Symbol('report'), 'mt': {'binding': 'pixl.plar.selection/1', 'asset_id': 'queue.working', 'plar_path': 'plar.txt', 'requirements_hash': selected['requirements_hash']}})
        document.records['member.task'].fields['ip'].append(Ref('selection'))
        document.records['member.task'].fields['st'] = Symbol('open')
        document.revision += 1
        store.commit(self.folder, document, expected, self.root)
        completion.complete(self.folder, codec.digest(document), 'member.task', ['member'], self.root)
        self.destination = self.root / 'assets/delivered.png'
        self.destination.parent.mkdir(exist_ok=True)
        shutil.copyfile(self.root / document.records['member'].fields['ur'], self.destination)

    def selected(self):
        return plar.read(self.root, asset_id='queue.working')['production']

    def finish_family(self):
        delivery.snapshot(self.folder, codec.digest(store.load(self.folder)), 'delivery.output', 'package', self.root)
        document = store.load(self.folder)
        expected = codec.digest(document)
        for criterion in ('q.continuity', 'q.delivery.engine'):
            add_verdict(document, self.root, 'package', criterion, 'pass', 'family.' + criterion)
        document.revision += 1
        store.commit(self.folder, document, expected, self.root)
        completion.complete(self.folder, codec.digest(document), 'delivery.task', ['package'], self.root)

    def test_current_destination_cannot_bypass_unfinished_collective_review(self):
        current = self.selected()
        self.assertEqual(current['next_action'], 'review_delivery')
        self.assertTrue(current['delivery']['destination_matches'])
        self.assertFalse(current['delivery']['complete'])
        self.finish_family()
        current = self.selected()
        self.assertEqual(current['next_action'], 'delivered')
        self.assertEqual(current['continuation']['action'], 'delivered')
        self.assertTrue(current['delivery']['families'][0]['accepted'])
        self.assertTrue((self.root / current['delivery']['families'][0]['manifest']).is_file())

    def test_changed_or_missing_destination_reopens_delivery_action(self):
        self.finish_family()
        self.assertEqual(self.selected()['next_action'], 'delivered')
        self.destination.write_bytes(b'changed after acceptance')
        current = self.selected()
        self.assertEqual(current['next_action'], 'review_delivery')
        self.assertFalse(current['delivery']['destination_matches'])
        self.destination.unlink()
        self.assertEqual(self.selected()['next_action'], 'review_delivery')

    def test_reopened_family_and_requirement_drift_are_not_delivered(self):
        self.finish_family()
        document = store.load(self.folder)
        expected = codec.digest(document)
        document.records['delivery.task'].fields['st'] = Symbol('open')
        document.revision += 1
        store.commit(self.folder, document, expected, self.root)
        self.assertEqual(self.selected()['next_action'], 'review_delivery')
        (self.root / 'BRIEF.md').write_text('Changed requirements', encoding='utf-8')
        current = self.selected()
        self.assertEqual(current['next_action'], 'review_contract')
        self.assertIsNone(current['delivery'])

    def test_changed_sibling_selection_keeps_family_delivery_open(self):
        queue = json.loads((self.root / 'plar.txt').read_bytes())
        other = next(a for a in queue['assets'] if a['id'] == 'queue.retry')
        other['production'] = {'store': '.pixl/family', 'task': 'other.task', 'output': 'other.output'}
        plar.save(self.root, queue, plar.read(self.root)['hash'])
        selected = plar.read(self.root, asset_id='queue.retry', include_production=False)
        path = self.root / 'other-selection.json'
        path.write_text(json.dumps(selected), encoding='utf-8')
        document = store.load(self.folder)
        expected = codec.digest(document)
        binding = copy.deepcopy(document.records['selection'])
        binding.id = 'other.selection'
        binding.fields.update(ur=path.name, dg=sha256(path.read_bytes()).hexdigest())
        binding.fields['mt'].update(asset_id='queue.retry', requirements_hash=selected['requirements_hash'])
        document.records[binding.id] = binding
        task = copy.deepcopy(document.records['member.task'])
        task.id = 'other.task'
        task.fields.update(st=Symbol('open'), ip=[Ref('sample'), Ref(binding.id)], op=[Ref('other.output')], ca=[], vr=[])
        document.records[task.id] = task
        output = copy.deepcopy(document.records['member.output'])
        output.id = 'other.output'
        output.fields['tk'] = Ref(task.id)
        document.records[output.id] = output
        candidate = copy.deepcopy(document.records['member'])
        candidate.id = 'other.candidate'
        candidate.fields['of'] = Ref(output.id)
        document.records[candidate.id] = candidate
        document.records['delivery.task'].fields['dp'].append(Ref(task.id))
        document.records['delivery.output'].fields['mb'].append(Ref(output.id))
        document.revision += 1
        store.commit(self.folder, document, expected, self.root)
        expected = codec.digest(document)
        for criterion in ('q.mechanical', 'q.member.continuity'):
            add_verdict(document, self.root, candidate.id, criterion, 'pass', 'other.' + criterion)
        document.revision += 1
        store.commit(self.folder, document, expected, self.root)
        completion.complete(self.folder, codec.digest(document), task.id, [candidate.id], self.root)
        self.finish_family()
        self.assertEqual(self.selected()['next_action'], 'delivered')
        queue = json.loads((self.root / 'plar.txt').read_bytes())
        next(a for a in queue['assets'] if a['id'] == 'queue.retry')['purpose'] += ' A changed sibling requirement.'
        plar.save(self.root, queue, plar.read(self.root)['hash'])
        current = self.selected()
        self.assertTrue(current['selection_current'])
        self.assertEqual(current['next_action'], 'review_delivery')
        self.assertFalse(current['delivery']['families'][0]['member_selection_current'])
        other = next(a for a in queue['assets'] if a['id'] == 'queue.retry')
        other['purpose'] = selected['asset']['purpose']
        other['production']['store'] = '.pixl/relinked-sibling'
        plar.save(self.root, queue, plar.read(self.root)['hash'])
        self.assertEqual(self.selected()['next_action'], 'review_delivery')


if __name__ == '__main__':
    unittest.main()
