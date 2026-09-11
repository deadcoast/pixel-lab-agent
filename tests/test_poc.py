from importlib import import_module, util
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from PIL import Image


class PocTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(util.find_spec('pixl.poc'), 'Executable POC runner has not been implemented')
        self.poc = import_module('pixl.poc')
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def run_checks(self):
        report = self.poc.run_all(self.root)
        return report, {item['id']: item for item in report['checks']}

    def test_report_contains_observed_evidence_and_valid_method_ids(self):
        report, checks = self.run_checks()
        self.assertEqual(report['status'], 'pass')
        self.assertGreaterEqual(len(checks), 16)
        self.assertEqual(len(checks), len(report['checks']))
        known = {m['id'] for m in json.loads(Path('knowledge/pixel-art.json').read_text(encoding='utf-8'))['methods']}
        for item in checks.values():
            self.assertEqual(item['status'], 'pass', item)
            self.assertTrue(item['observed'])
            self.assertTrue(item['expected'])
            self.assertTrue(item['limitations'])
            self.assertTrue(item['method_ids'])
            self.assertTrue(set(item['method_ids']) <= known)
        self.assertEqual({method for item in checks.values() for method in item['method_ids']}, known)
        self.assertEqual(json.loads((self.root / 'poc-report.json').read_text(encoding='utf-8')), report)
        json.dumps(report, allow_nan=False)

    def test_dither_coverage_uses_counted_populations(self):
        _, checks = self.run_checks()
        self.assertEqual(checks['dither-coverage-4x4']['observed']['counts'], [4, 8, 12])
        self.assertEqual(checks['dither-phase-cycle']['observed']['counts'], [8, 8, 8, 8, 8])
        self.assertTrue(checks['dither-phase-cycle']['observed']['returns_to_start'])

    def test_terrain_fixture_checks_all_pairs_with_corner_orientation(self):
        _, checks = self.run_checks()
        observed = checks['corner-topology-pairs']['observed']
        self.assertEqual(observed['pairs_per_axis'], 256)
        self.assertEqual(observed['compatible_per_axis'], [64, 64])
        self.assertEqual(observed['oracle_mismatches'], [])
        self.assertEqual(observed['right_of_2'], [1, 3, 5, 7])
        self.assertEqual(observed['below_8'], [1, 5, 9, 13])

    def test_palette_fixture_detects_mutant_and_clamps_light_bands(self):
        _, checks = self.run_checks()
        self.assertEqual(checks['palette-membership']['observed'], {'valid_violations': [], 'mutant_violations': [[2, 1]]})
        self.assertEqual(checks['palette-band-bounds']['observed']['indices'], [0, 0, 1, 2, 2, 3, 3])
        self.assertTrue(checks['palette-band-bounds']['observed']['rejects_nan'])

    def test_crop_roundtrip_preserves_original_anchor(self):
        _, checks = self.run_checks()
        observed = checks['crop-anchor-roundtrip']['observed']
        self.assertEqual(observed, {'crop_size': [4, 5], 'trim_offset': [6, 7], 'local_anchor': [2, 4], 'restored_anchor': [8, 11], 'pixels_equal': True})

    def test_timeline_samples_authored_millisecond_boundaries(self):
        _, checks = self.run_checks()
        self.assertEqual(checks['frame-boundaries']['observed']['frames'], ['A', 'A', 'B', 'B', 'C', 'C', 'A'])

    def test_subpixel_fixtures_measure_mass_centroids_and_silhouette(self):
        _, checks = self.run_checks()
        self.assertEqual(checks['edge-coverage-centroid']['observed']['centroids'], [0, 0.25, 0.5, 0.75, 1])
        self.assertEqual(checks['cluster-handoff-centroid']['observed'], {'areas': [2, 3, 2], 'centroids': [1.5, 2, 2.5], 'components': [1, 1, 1]})
        self.assertEqual(checks['shading-drift-mask']['observed']['changed_pixels'], 2)
        self.assertTrue(checks['shading-drift-mask']['observed']['same_silhouette'])

    def test_rig_fixture_exercises_parent_rotation_and_attachment_pivots(self):
        _, checks = self.run_checks()
        self.assertEqual(checks['rig-pivot-hierarchy']['observed'], {'socket_world': [3, 32], 'attachment_world_pivots': [[3, 32], [3, 32]], 'mutant_error': 1})
        self.assertEqual(checks['final-snap-state']['observed']['rendered'], [0, 1, 1, 1, 1, 2, 2, 2])
        self.assertEqual(checks['final-snap-state']['observed']['continuous_end'], 2)

    def test_normal_fixture_detects_axis_direction_and_quantization_error(self):
        _, checks = self.run_checks()
        normal = checks['normal-orientation']['observed']
        self.assertEqual(normal['responses'], [[1, 0, 0.5, 0.5], [0, 1, 0.5, 0.5], [0.5, 0.5, 1, 0], [0.5, 0.5, 0, 1]])
        self.assertLess(normal['maximum_8bit_angular_error_deg'], 1)
        self.assertEqual(checks['shadow-occlusion']['observed']['visibility'], [0, 1])

    def test_cell_world_preserves_entities_and_records_per_tick_bounds(self):
        _, checks = self.run_checks()
        cell = checks['cell-conservation-determinism']['observed']
        self.assertEqual(cell['first_tick'], [[1, 3, 2], [2, 3, 3], [3, 4, 2]])
        self.assertEqual(cell['particle_counts'], [3] * 21)
        self.assertEqual(cell['maximum_moves_per_id_per_tick'], 1)
        self.assertTrue(cell['same_seed_same_states'])
        self.assertTrue(cell['displacement_bound_holds'])

    def test_destructible_bridge_splits_without_lost_or_duplicated_cells(self):
        _, checks = self.run_checks()
        self.assertEqual(checks['destruction-components']['observed'], {'before_sizes': [19], 'after_sizes': [9, 9], 'union_size': 18, 'overlap_size': 0})
        self.assertEqual(checks['cluster-connectivity']['observed']['four_neighbor_sizes'], [1, 1, 1, 4])
        self.assertEqual(checks['cluster-connectivity']['observed']['eight_neighbor_sizes'], [1, 2, 4])

    def test_artifact_hashes_match_files_and_nearest_pixels_are_uniform(self):
        report, _ = self.run_checks()
        self.assertTrue(report['artifacts'])
        for artifact in report['artifacts']:
            path = self.root / artifact['path']
            self.assertEqual(sha256(path.read_bytes()).hexdigest(), artifact['sha256'])
        with Image.open(self.root / 'integer-upscale.png') as image:
            self.assertEqual(image.size, (6, 6))
            self.assertEqual(image.getpixel((0, 0)), (255, 0, 0, 255))
            self.assertEqual(image.getpixel((2, 2)), (255, 0, 0, 255))
            self.assertEqual(image.getpixel((3, 0)), (0, 255, 0, 255))
            self.assertEqual(image.getpixel((0, 3)), (0, 0, 255, 255))
            self.assertEqual(image.getpixel((5, 5)), (255, 255, 0, 255))

    def test_repeated_runs_are_deterministic_and_accept_string_paths(self):
        first = self.poc.run_all(str(self.root / 'first'))
        second = self.poc.run_all(self.root / 'second')
        self.assertEqual(first, second)

    def test_broken_algorithm_is_a_failed_report_not_a_fabricated_pass(self):
        with patch.object(self.poc, '_dither_mask', return_value=[[False] * 4 for _ in range(4)]):
            report, checks = self.run_checks()
        self.assertEqual(report['status'], 'fail')
        self.assertEqual(checks['dither-coverage-4x4']['status'], 'fail')
        self.assertEqual(checks['dither-coverage-4x4']['observed']['counts'], [0, 0, 0])
        self.assertEqual(checks['destruction-components']['status'], 'pass')

    def test_fixture_exception_is_recorded_and_later_checks_still_run(self):
        with patch.object(self.poc, '_dither_mask', side_effect=ValueError('intentional fixture failure')):
            report, checks = self.run_checks()
        self.assertEqual(report['status'], 'fail')
        self.assertEqual(checks['dither-coverage-4x4']['status'], 'fail')
        self.assertIn('intentional fixture failure', checks['dither-coverage-4x4']['observed']['error'])
        self.assertEqual(checks['destruction-components']['status'], 'pass')

    def observation(self, identifier):
        _, checks = self.run_checks()
        self.assertTrue(identifier in checks, f'{identifier} still has no executable proof')
        self.assertEqual(checks[identifier]['status'], 'pass', checks[identifier])
        return checks[identifier]['observed']

    def test_representation_owner_uses_independent_behavior_domains(self):
        self.assertEqual(self.observation('representation-domain-classification'), {
            'owners': [['cell'], ['attachment'], ['frame'], ['cluster'], ['surface-channel'], ['occlusion']],
            'normal_and_shadow': ['surface-channel', 'occlusion'], 'normal_alone_satisfies_shadow': False})

    def test_silhouette_detects_filled_hole_and_merged_teeth(self):
        observed = self.observation('key-silhouette-landmarks')
        self.assertEqual(observed, {'positive': {'hole': True, 'shaft': True, 'teeth': 2},
                                    'negative': {'hole': False, 'shaft': True, 'teeth': 1}})
        with Image.open(self.root / 'key-positive.png') as image:
            self.assertEqual(image.size, (16, 16))
            self.assertEqual(image.getpixel((4, 6))[3], 0)
            self.assertEqual(image.getpixel((11, 9))[3], 0)
        with Image.open(self.root / 'key-negative.png') as image:
            self.assertEqual(image.getpixel((4, 6))[3], 255)
            self.assertEqual(image.getpixel((11, 9))[3], 255)
        with Image.open(self.root / 'key-contact-sheet.png') as sheet:
            self.assertEqual(sheet.size, (288, 176))

    def test_edge_rhythm_flags_detour_but_honors_intentional_regions(self):
        self.assertEqual(self.observation('edge-rhythm-detour'), {
            'baseline_deviations': [], 'detour_deviations': [[5, 4], [5, 5]],
            'accidental_correction_candidates': [[5, 4], [5, 5]], 'intentional_correction_candidates': []})

    def test_selective_aa_rejects_mutant_outside_selected_edge(self):
        self.assertEqual(self.observation('selective-aa-boundary'), {
            'valid_changes': [[1, 0], [2, 1]], 'valid_forbidden_changes': [],
            'mutant_forbidden_changes': [[2, 2]], 'palette_violations': []})

    def test_tile_repeat_detects_exact_border_mismatch_in_neighborhood(self):
        self.assertEqual(self.observation('tile-repeat-neighborhood'), {
            'original_mismatches': [], 'mutant_mismatches': [['horizontal', 3]], 'neighborhood_size': [24, 24]})

    def test_tile_variant_sequence_has_literal_seeded_oracle(self):
        self.assertEqual(self.observation('seeded-tile-variants'), {
            'first_cycle': [0, 0, 0, 1, 2, 2, 2, 0, 2, 1, 1, 2, 1, 0, 0, 1],
            'selection_count': 64, 'four_literal_cycles': True, 'repeatable': True,
            'valid_variant_mismatches': [0, 0, 0], 'mutant_mismatch_count': 1})

    def test_provenance_manifest_keeps_unresolved_reuse_visible(self):
        self.assertEqual(self.observation('provenance-manifest'), {
            'declared_original_assets': ['folder-original'], 'unresolved_reuse_assets': ['npc-reference'],
            'release_manifest_complete': False})

    def test_alpha_contract_distinguishes_models_and_binary_alpha(self):
        self.assertEqual(self.observation('alpha-compositing-contract'), {
            'straight_result': [127.5, 0, 127.5], 'premultiplied_result': [127.5, 0, 127.5],
            'double_multiplied_mutant': [63.75, 0, 127.5], 'binary_alpha_violations': [2]})

    def test_animation_channels_do_not_reset_unrelated_phase(self):
        self.assertEqual(self.observation('independent-animation-channels'), {
            'tread_indices': [0, 1, 2, 3, 0, 1, 2, 3], 'recoil_offsets': [0, 0, 0, 0, -2, -1, 0, 0],
            'armor_states': ['normal', 'normal', 'normal', 'normal', 'normal', 'damaged', 'damaged', 'damaged']})

    def test_atlas_budget_reports_raw_bytes_without_claiming_resident_memory(self):
        self.assertEqual(self.observation('atlas-raw-storage-budget'), {
            'baked_rgba8_bytes': 60000000, 'modular_rgba8_bytes': 2621440})

    def test_channel_alignment_detects_shift_despite_matching_dimensions(self):
        self.assertEqual(self.observation('companion-pixel-alignment'), {
            'matching_dimensions': True, 'aligned_feature_mismatches': [], 'mutant_dimensions_match': True,
            'mutant_feature_mismatches': [[2, 5], [3, 5]]})

    def test_dirty_chunks_wake_across_boundary_and_match_full_scan(self):
        self.assertEqual(self.observation('dirty-region-boundary-parity'), {
            'positions': [[7, 1], [8, 2], [8, 3], [8, 4], [8, 5], [8, 6], [8, 6], [8, 6], [8, 6]],
            'states_match_each_tick': True, 'first_wakeup_chunks': [0, 1],
            'final_active_chunks': [], 'full_cell_visits': 1024, 'dirty_cell_visits': 704})

    def test_reaction_table_rejects_invalid_probability_and_respects_threshold(self):
        self.assertEqual(self.observation('reaction-threshold-table'), {
            'outputs': ['water', 'steam', 'steam'], 'occupied_cells': 3,
            'invalid_probability_rejected': True, 'unknown_material_rejected': True})

    def test_pipeline_dependency_order_detects_presentation_before_lighting(self):
        self.assertEqual(self.observation('pipeline-dependency-order'), {
            'valid_violations': [], 'mutant_violations': ['light->upscale']})

    def test_ui_visual_state_tracks_real_input_and_disabled_state(self):
        self.assertEqual(self.observation('input-driven-pixel-ui'), {
            'states': ['idle', 'pressed', 'idle', 'disabled', 'disabled'], 'distinct_state_masks': 3})

    def test_lost_cross_chunk_wakeup_produces_failed_evidence(self):
        self.assertTrue(hasattr(self.poc, '_wake_chunks'), 'Dirty-region wakeup primitive is not implemented')
        with patch.object(self.poc, '_wake_chunks', return_value={0}):
            report, checks = self.run_checks()
        self.assertEqual(report['status'], 'fail')
        self.assertEqual(checks['dirty-region-boundary-parity']['status'], 'fail')
        self.assertFalse(checks['dirty-region-boundary-parity']['observed']['states_match_each_tick'])
        self.assertEqual(checks['destruction-components']['status'], 'pass')


if __name__ == '__main__':
    unittest.main()
