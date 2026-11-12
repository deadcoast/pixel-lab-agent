"""An accepted member is delivered only at its destination and with its family."""

import copy
import json
import shutil
import unittest
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import codec, completion, delivery, plar, store
from pixl.codec import Record, Ref, Symbol
from tests.family_support import family
from tests.lifecycle_support import add_candidate, add_verdict
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


class PLARFamilyDirectoryDeliveryTests(unittest.TestCase):
    """Directory delivery follows actual manifest paths, not similar filenames."""

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'consumer'
        seed(self.root)
        self.folder = self.root / '.pixl/family'

    selected = PLARFamilyDeliveryTests.selected
    finish_family = PLARFamilyDeliveryTests.finish_family

    def prepare_family(self, locations=None, destination='assets/delivery'):
        locations = locations or {}

        def placed_candidate(document, root, candidate_id):
            result = add_candidate(document, root, candidate_id)
            record = document.records[candidate_id]
            source = root / record.fields['ur']
            target = root / locations.get(candidate_id, f'assets/delivery/{candidate_id}.png')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(source, target)
            record.fields['ur'] = target.relative_to(root).as_posix()
            return result

        with patch('tests.family_support.add_candidate', side_effect=placed_candidate):
            family(self.root, self.folder)
        queue = json.loads((self.root / 'plar.txt').read_bytes())
        asset = next(a for a in queue['assets'] if a['id'] == 'queue.working')
        asset['production'] = {'store': '.pixl/family', 'task': 'delivery.task', 'output': 'delivery.output'}
        asset['delivery']['path'] = destination
        plar.save(self.root, queue, plar.read(self.root)['hash'])
        selected = plar.read(self.root, asset_id='queue.working', include_production=False)
        snapshot = self.root / 'selection.json'
        snapshot.write_text(json.dumps(selected), encoding='utf-8')
        document = store.load(self.folder)
        expected = codec.digest(document)
        document.records['selection'] = Record('selection', 'X', {
            'nm': 'Current synthetic family selection', 'ur': 'selection.json',
            'dg': sha256(snapshot.read_bytes()).hexdigest(), 'kd': Symbol('report'),
            'mt': {'binding': 'pixl.plar.selection/1', 'asset_id': 'queue.working',
                   'plar_path': 'plar.txt', 'requirements_hash': selected['requirements_hash']},
        })
        document.records['delivery.task'].fields['ip'].append(Ref('selection'))
        document.revision += 1
        store.commit(self.folder, document, expected, self.root)

    def test_linked_accepted_family_observes_exact_directory_members_read_only(self):
        self.prepare_family()
        self.finish_family()
        unrelated = self.root / 'assets/delivery/unrelated.png'
        unrelated.write_bytes(b'not part of the manifest')
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = self.selected()
        self.assertEqual(result['next_action'], 'delivered')
        observed = result['delivery']
        self.assertTrue(observed['complete'])
        self.assertEqual(observed['destination_kind'], 'directory')
        self.assertIsNone(observed['expected_sha256'])
        self.assertIsNone(observed['observed_sha256'])
        self.assertEqual([r['source_path'] for r in observed['destination_files']],
                         ['assets/delivery/sample.png', 'assets/delivery/member.png'])
        self.assertTrue(all(r['destination_matches'] for r in observed['destination_files']))
        self.assertEqual(observed['families'][0]['output'], 'delivery.output')
        self.assertTrue(observed['families'][0]['accepted'])
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_missing_or_tampered_member_cannot_use_intact_retained_copy(self):
        self.prepare_family()
        self.finish_family()
        path = self.root / 'assets/delivery/member.png'
        original = path.read_bytes()
        for change in ('missing', 'tampered'):
            with self.subTest(change=change):
                path.unlink() if change == 'missing' else path.write_bytes(b'tampered')
                self.assertNotEqual(self.selected()['next_action'], 'delivered')
                path.write_bytes(original)
        self.assertEqual(self.selected()['next_action'], 'delivered')

    def test_copied_basename_cannot_replace_manifest_source_outside_directory(self):
        self.prepare_family({'member': 'work/member.png'})
        self.finish_family()
        shutil.copyfile(self.root / 'work/member.png', self.root / 'assets/delivery/member.png')
        result = self.selected()
        self.assertEqual(result['next_action'], 'review_delivery')
        self.assertFalse(result['delivery']['complete'])
        member = result['delivery']['destination_files'][1]
        self.assertFalse(member['within_destination'])
        self.assertIsNone(member['observed_sha256'])

    def test_duplicate_consumer_path_cannot_satisfy_two_members(self):
        self.prepare_family({'sample': 'assets/delivery/shared.png', 'member': 'assets/delivery/shared.png'})
        self.finish_family()
        result = self.selected()
        self.assertEqual(result['next_action'], 'review_delivery')
        self.assertFalse(result['delivery']['complete'])
        self.assertTrue(result['delivery']['destination_files'][1]['duplicate_destination'])

    def test_retained_unaccepted_package_is_not_delivery(self):
        self.prepare_family()
        delivery.snapshot(self.folder, codec.digest(store.load(self.folder)), 'delivery.output', 'package', self.root)
        result = self.selected()
        self.assertTrue(result['selection_current'])
        self.assertNotEqual(result['next_action'], 'delivered')
        self.assertIsNone(result['delivery'])

    def test_historical_package_does_not_accept_a_revised_family_plan(self):
        self.prepare_family()
        self.finish_family()
        document = store.load(self.folder)
        expected = codec.digest(document)
        document.records['delivery.task'].fields['st'] = Symbol('open')
        for reference in document.records['delivery.task'].fields['vr']:
            verdict = document.records[reference.id]
            verdict.fields['ob'] = True
            for evidence in verdict.fields['ev']:
                document.records[evidence.id].fields['ob'] = True
        document.records['delivery.output'].fields['mb'].reverse()
        document.revision += 1
        store.commit(self.folder, document, expected, self.root)
        self.assertTrue(delivery.report(store.load(self.folder), self.root)['families'][0]['snapshots'][0]['stale'])
        self.assertNotEqual(self.selected()['next_action'], 'delivered')

    def test_current_requirements_remain_required_for_directory_delivery(self):
        self.prepare_family()
        self.finish_family()
        queue = json.loads((self.root / 'plar.txt').read_bytes())
        next(a for a in queue['assets'] if a['id'] == 'queue.working')['purpose'] += ' Changed requirement.'
        plar.save(self.root, queue, plar.read(self.root)['hash'])
        result = self.selected()
        self.assertEqual(result['next_action'], 'review_contract')
        self.assertIsNone(result['delivery'])

    def test_pending_member_job_blocks_an_otherwise_accepted_directory(self):
        self.prepare_family()
        self.finish_family()
        document = store.load(self.folder)
        expected = codec.digest(document)
        document.records['pending'] = Record('pending', 'J', {
            'tk': Ref('member.task'), 'tl': 'synthetic', 'ah': 'a' * 64,
            'si': Symbol('unknown'), 'ri': '', 'ev': [],
        })
        document.revision += 1
        store.commit(self.folder, document, expected, self.root)
        result = self.selected()
        self.assertEqual(result['next_action'], 'review_delivery')
        self.assertTrue(result['delivery']['destination_matches'])
        self.assertFalse(result['delivery']['families'][0]['accepted'])
        self.assertFalse(result['delivery']['complete'])

    def test_family_manifest_can_still_be_a_single_file_destination(self):
        self.prepare_family(destination='assets/package.json')
        self.finish_family()
        document = store.load(self.folder)
        shutil.copyfile(self.root / document.records['package'].fields['ur'], self.root / 'assets/package.json')
        result = self.selected()
        self.assertEqual(result['next_action'], 'delivered')
        self.assertEqual(result['delivery']['expected_sha256'], result['delivery']['observed_sha256'])
        self.assertNotIn('destination_kind', result['delivery'])


if __name__ == '__main__':
    unittest.main()
