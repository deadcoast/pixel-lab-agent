"""Deterministic, offline proofs of bounded pixel-art mechanics.

These are executable reference fixtures, not tests of an external image service
or promises that a game engine implements the same systems. Each observation is
compared with hand-derived fixture expectations or an explicit invariant. No
network, renderer, account or external source code is involved.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
import math
from pathlib import Path
from typing import Callable

from PIL import Image, __version__ as pillow_version


_BAYER = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))
_PALETTE = ((16, 24, 32, 255), (64, 96, 80, 255), (144, 176, 112, 255), (224, 216, 144, 255))


def _dither_mask(threshold: int) -> list[list[bool]]:
    return [[rank < threshold for rank in row] for row in _BAYER]


def _components(points: set[tuple[int, int]], diagonal: bool = False) -> list[set]:
    pending = set(points)
    components = []
    steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if diagonal:
        steps += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    while pending:
        seed = min(pending)
        pending.remove(seed)
        found, queue = {seed}, [seed]
        while queue:
            x, y = queue.pop()
            for dx, dy in steps:
                neighbor = (x + dx, y + dy)
                if neighbor in pending:
                    pending.remove(neighbor)
                    found.add(neighbor)
                    queue.append(neighbor)
        components.append(found)
    return components


def _palette_violations(image: Image.Image) -> list[list[int]]:
    return [[x, y] for y in range(image.height) for x in range(image.width)
            if image.getpixel((x, y)) not in _PALETTE]


def _band(intensity: float, count: int = 4) -> int:
    if not math.isfinite(intensity) or count < 2:
        raise ValueError('Light intensity must be finite and band count at least two')
    return math.floor(min(1.0, max(0.0, intensity)) * (count - 1) + 0.5)


def _corner_match(left: int, right: int, axis: str) -> bool:
    # Bit assignment is TL=1, TR=2, BR=4, BL=8, unlike an edge-mask set.
    if axis == 'horizontal':
        return bool(left & 2) == bool(right & 1) and bool(left & 4) == bool(right & 8)
    return bool(left & 8) == bool(right & 1) and bool(left & 4) == bool(right & 2)


def _at_time(frames: list[tuple[str, int]], time_ms: int) -> str:
    if not frames or any(duration <= 0 for _, duration in frames):
        raise ValueError('Animation requires frames with positive durations')
    local = time_ms % sum(duration for _, duration in frames)
    for name, duration in frames:
        if local < duration:
            return name
        local -= duration
    raise AssertionError('Unreachable timeline state')


def _place(point: tuple[float, float], translation: tuple[float, float], degrees: float) -> list[float]:
    angle = math.radians(degrees)
    x, y = point
    return [round(x * math.cos(angle) - y * math.sin(angle) + translation[0], 9),
            round(x * math.sin(angle) + y * math.cos(angle) + translation[1], 9)]


def _normalize(vector) -> tuple[float, ...]:
    length = math.sqrt(sum(value * value for value in vector))
    if not length or not math.isfinite(length):
        raise ValueError('Normal vector must have finite nonzero length')
    return tuple(value / length for value in vector)


def _sand(seed: int) -> tuple[list, list]:
    # Persistent particle IDs make duplicate movement observable. This bounded
    # model has powder, a floor and one-cell moves, not general fluid chemistry.
    grid = {(3, 1): 1, (3, 2): 2, (4, 1): 3}
    states = [dict(grid)]
    move_logs = []
    for tick in range(20):
        updated = set()
        moves = []
        for y in range(6, -1, -1):
            for x in (range(8) if tick % 2 == 0 else range(7, -1, -1)):
                particle = grid.get((x, y))
                if particle is None or particle in updated:
                    continue
                updated.add(particle)
                direction = 1 if (seed ^ (x * 73856093) ^ (y * 19349663) ^ (tick * 83492791)) & 1 else -1
                for nx, ny in ((x, y + 1), (x + direction, y + 1), (x - direction, y + 1)):
                    if 0 <= nx < 8 and ny < 7 and (nx, ny) not in grid:
                        del grid[(x, y)]
                        grid[(nx, ny)] = particle
                        moves.append((particle, x, y, nx, ny))
                        break
        states.append(dict(grid))
        move_logs.append(moves)
    return states, move_logs


def run_all(output_dir: Path | str) -> dict:
    """Run reference fixtures, write PNG evidence and poc-report.json, return it.

    Filesystem errors propagate rather than claiming a report was saved. An
    individual fixture's exception is recorded as a failed check and does not
    suppress subsequent checks. Re-running the same implementation produces the
    same report; wall-clock timestamps are deliberately not simulated evidence.
    """
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    checks = []
    artifacts = []

    def save_image(name: str, image: Image.Image) -> None:
        path = output / name
        image.save(path, format='PNG')
        artifacts.append({'path': name, 'sha256': sha256(path.read_bytes()).hexdigest(),
                          'width': image.width, 'height': image.height, 'mode': image.mode})

    def check(identifier: str, method_ids: list[str], expected: dict,
              operation: Callable[[], dict], limitations: str,
              accepts: Callable[[dict], bool] | None = None) -> None:
        try:
            observed = operation()
            json.dumps(observed, allow_nan=False)
            passed = accepts(observed) if accepts else observed == expected
        except Exception as error:
            observed = {'error': f'{type(error).__name__}: {error}'}
            passed = False
        checks.append({'id': identifier, 'method_ids': method_ids,
                       'status': 'pass' if passed else 'fail', 'observed': observed,
                       'expected': expected, 'limitations': limitations})

    def dither_coverage():
        masks = [_dither_mask(value) for value in (4, 8, 12)]
        image = Image.new('RGBA', (12, 4))
        for index, mask in enumerate(masks):
            for y, row in enumerate(mask):
                for x, occupied in enumerate(row):
                    image.putpixel((index * 4 + x, y), (255, 255, 255, 255) if occupied else (0, 0, 0, 255))
        save_image('dither-coverage.png', image)
        return {'counts': [sum(sum(row) for row in mask) for mask in masks]}

    check('dither-coverage-4x4', ['dither-coverage'], {'counts': [4, 8, 12]}, dither_coverage,
          'Counts only this specified 4x4 ordered pattern; does not establish texture quality.')

    def dither_phase():
        start = _dither_mask(8)
        frames = [[[start[y][(x - phase) % 4] for x in range(4)] for y in range(4)] for phase in range(5)]
        return {'counts': [sum(sum(row) for row in frame) for frame in frames], 'returns_to_start': frames[0] == frames[-1]}

    check('dither-phase-cycle', ['dither-phase-motion'], {'counts': [8, 8, 8, 8, 8], 'returns_to_start': True},
          dither_phase, 'Proves coverage and periodicity, not comfort, directional readability or absence of visual flicker.')

    def palette_membership():
        image = Image.new('RGBA', (4, 4))
        image.putdata([_PALETTE[index % 4] for index in range(16)])
        valid = _palette_violations(image)
        image.putpixel((2, 1), (64, 96, 81, 255))
        return {'valid_violations': valid, 'mutant_violations': _palette_violations(image)}

    check('palette-membership', ['palette-contract'], {'valid_violations': [], 'mutant_violations': [[2, 1]]},
          palette_membership, 'Exact RGBA membership for an opaque fixture; no claim about palette taste or perceptual distance.')

    def palette_bands():
        bands = [_band(value) for value in (-1, 0, .2, .5, .8, 1, 2)]
        rejected = False
        try:
            _band(float('nan'))
        except ValueError:
            rejected = True
        return {'indices': bands, 'output_colors': [list(_PALETTE[index]) for index in bands], 'rejects_nan': rejected}

    check('palette-band-bounds', ['palette-lighting', 'material-ramps'],
          {'indices': [0, 0, 1, 2, 2, 3, 3], 'output_colors': [[16,24,32,255],[16,24,32,255],
           [64,96,80,255],[144,176,112,255],[144,176,112,255],[224,216,144,255],[224,216,144,255]],
           'rejects_nan': True}, palette_bands,
          'Tests an explicit four-band ramp lookup, not an engine shader, color-management path or temporal lighting quality.')

    def corner_pairs():
        # These literal allowed-neighbor tables are the independent oracle,
        # enumerated from a paper drawing of TL/TR/BR/BL corner labels.
        right_oracle = [(0,2,4,6), (0,2,4,6), (1,3,5,7), (1,3,5,7),
                        (8,10,12,14), (8,10,12,14), (9,11,13,15), (9,11,13,15),
                        (0,2,4,6), (0,2,4,6), (1,3,5,7), (1,3,5,7),
                        (8,10,12,14), (8,10,12,14), (9,11,13,15), (9,11,13,15)]
        below_oracle = [(0,4,8,12), (0,4,8,12), (0,4,8,12), (0,4,8,12),
                        (2,6,10,14), (2,6,10,14), (2,6,10,14), (2,6,10,14),
                        (1,5,9,13), (1,5,9,13), (1,5,9,13), (1,5,9,13),
                        (3,7,11,15), (3,7,11,15), (3,7,11,15), (3,7,11,15)]
        totals, mismatches = [], []
        for axis, oracle in (('horizontal', right_oracle), ('vertical', below_oracle)):
            total = 0
            for a in range(16):
                for b in range(16):
                    actual = _corner_match(a, b, axis)
                    total += actual
                    if actual != (b in oracle[a]):
                        mismatches.append([axis, a, b])
            totals.append(total)
        return {'pairs_per_axis': 256, 'compatible_per_axis': totals, 'oracle_mismatches': mismatches,
                'right_of_2': [b for b in range(16) if _corner_match(2, b, 'horizontal')],
                'below_8': [b for b in range(16) if _corner_match(8, b, 'vertical')]}

    check('corner-topology-pairs', ['terrain-topology'],
          {'pairs_per_axis': 256, 'compatible_per_axis': [64, 64], 'oracle_mismatches': [],
           'right_of_2': [1, 3, 5, 7], 'below_8': [1, 5, 9, 13]}, corner_pairs,
          'Checks binary corner-label compatibility, not visual seams, 47-tile blob completeness or provider tile ordering.')

    def crop_anchor():
        image = Image.new('RGBA', (16, 16))
        for y in range(7, 12):
            for x in range(6, 10):
                image.putpixel((x, y), _PALETTE[2])
        bounds = image.getchannel('A').getbbox()
        cropped = image.crop(bounds)
        anchor = (8, 11)
        local = [anchor[0] - bounds[0], anchor[1] - bounds[1]]
        restored = Image.new('RGBA', image.size)
        restored.paste(cropped, bounds[:2])
        save_image('crop-restored.png', restored)
        return {'crop_size': list(cropped.size), 'trim_offset': list(bounds[:2]), 'local_anchor': local,
                'restored_anchor': [local[0] + bounds[0], local[1] + bounds[1]],
                'pixels_equal': restored.tobytes() == image.tobytes()}

    check('crop-anchor-roundtrip', ['crop-and-anchor'],
          {'crop_size': [4, 5], 'trim_offset': [6, 7], 'local_anchor': [2, 4],
           'restored_anchor': [8, 11], 'pixels_equal': True}, crop_anchor,
          'Tests transparent-padding trimming, not automatic segmentation of a painted background.')

    def integer_upscale():
        colors = [(255,0,0,255), (0,255,0,255), (0,0,255,255), (255,255,0,255)]
        image = Image.new('RGBA', (2, 2))
        image.putdata(colors)
        scaled = image.resize((6, 6), Image.Resampling.NEAREST)
        uniform = []
        for index, (ox, oy) in enumerate(((0,0), (3,0), (0,3), (3,3))):
            uniform.append(all(scaled.getpixel((ox+x, oy+y)) == colors[index] for y in range(3) for x in range(3)))
        save_image('integer-upscale.png', scaled)
        return {'size': list(scaled.size), 'uniform_blocks': uniform,
                'color_count': len({scaled.getpixel((x,y)) for y in range(6) for x in range(6)})}

    check('integer-nearest-upscale', ['integer-presentation'],
          {'size': [6,6], 'uniform_blocks': [True,True,True,True], 'color_count': 4}, integer_upscale,
          'Pillow output-pixel proof only; browser zoom, device pixel ratio, camera transforms and engine sampling remain untested.')

    check('frame-boundaries', ['frame-timing'], {'frames': ['A','A','B','B','C','C','A']},
          lambda: {'frames': [_at_time([('A',80),('B',40),('C',120)], t) for t in (0,79,80,119,120,239,240)]},
          'Tests looping frame selection with half-open intervals, not audiovisual synchronization or action-event dispatch.')

    def edge_centroids():
        frames = [(1,0),(.75,.25),(.5,.5),(.25,.75),(0,1)]
        return {'masses': [sum(frame) for frame in frames],
                'centroids': [sum(x*value for x,value in enumerate(frame))/sum(frame) for frame in frames]}

    check('edge-coverage-centroid', ['edge-color-migration'],
          {'masses': [1,1,1,1,1], 'centroids': [0,.25,.5,.75,1]}, edge_centroids,
          'Coverage centroid is a numerical motion cue, not proof that a viewer perceives an equally spaced movement.')

    def handoff():
        frames = ['.##..', '.###.', '..##.']
        points = [{(x,0) for x,c in enumerate(frame) if c=='#'} for frame in frames]
        return {'areas': [len(p) for p in points], 'centroids': [sum(x for x,y in p)/len(p) for p in points],
                'components': [len(_components(p)) for p in points]}

    check('cluster-handoff-centroid', ['cluster-handoff'],
          {'areas': [2,3,2], 'centroids': [1.5,2,2.5], 'components': [1,1,1]}, handoff,
          'The temporary three-cell area is an explicit fixture allowance; rigid-feature volume and animation quality need review.')

    def shading_drift():
        first = Image.new('RGBA', (8,8))
        for y in range(1,7):
            for x in range(1,7):
                first.putpixel((x,y), _PALETTE[1])
        first.putpixel((2,3), _PALETTE[3])
        first.putpixel((3,3), _PALETTE[3])
        second = first.copy()
        second.putpixel((2,3), _PALETTE[1])
        second.putpixel((4,3), _PALETTE[3])
        pixels = [[im.getpixel((x,y)) for y in range(8) for x in range(8)] for im in (first,second)]
        return {'changed_pixels': sum(a != b for a,b in zip(*pixels)),
                'same_silhouette': first.getchannel('A').tobytes() == second.getchannel('A').tobytes(),
                'highlight_areas': [sum(pixel == _PALETTE[3] for pixel in frame) for frame in pixels]}

    check('shading-drift-mask', ['shading-drift', 'animation-anchors'],
          {'changed_pixels': 2, 'same_silhouette': True, 'highlight_areas': [2,2]}, shading_drift,
          'Proves mask preservation in this idle fixture, not a convincing breathing action or general world-space foot planting.')

    def coverage_candidate():
        source = Image.new('L', (5,5))
        source.putpixel((2,2), 255)
        high = source.resize((20,20), Image.Resampling.NEAREST)
        shifted = Image.new('L', (20,20))
        shifted.paste(high, (1,0))
        coverage = []
        for y in range(5):
            for x in range(5):
                value = sum(shifted.getpixel((x*4+dx,y*4+dy)) / 255 for dy in range(4) for dx in range(4)) / 16
                if value:
                    coverage.append([x,y,value])
        return {'nonzero_coverage': coverage, 'total_coverage': sum(p[2] for p in coverage)}

    check('supersampled-coverage', ['coverage-candidates'],
          {'nonzero_coverage': [[2,2,.75],[3,2,.25]], 'total_coverage': 1}, coverage_candidate,
          'Tests offline coverage construction; palette cleanup and artistic acceptance remain separate.')

    def rig_pivots():
        parent = (10,20)
        socket = _place((12,7), parent, 90)
        a = _place((2,3), (10,4), 0)
        b = _place((5,1), (7,6), 0)
        bad = _place((5,1), (8,6), 0)
        world = [_place(point,parent,90) for point in (a,b)]
        bad_world = _place(bad,parent,90)
        return {'socket_world': socket, 'attachment_world_pivots': world,
                'mutant_error': round(math.dist(socket,bad_world),9)}

    check('rig-pivot-hierarchy', ['rig-sockets','rig-cutout'],
          {'socket_world': [3,32], 'attachment_world_pivots': [[3,32],[3,32]], 'mutant_error': 1}, rig_pivots,
          'A two-level rigid coordinate proof; attachment artwork, inverse kinematics and a game-engine rig are not evaluated.')

    def snap_state():
        position = 0.0
        rendered = []
        for _ in range(8):
            position += .25
            rendered.append(math.floor(position+.5))
        return {'rendered': rendered, 'continuous_end': position}

    check('final-snap-state', ['continuous-state-final-snap'],
          {'rendered': [0,1,1,1,1,2,2,2], 'continuous_end': 2}, snap_state,
          'Uses nonnegative round-half-up positions; camera transforms, negative tie behavior and independent bone seams need separate fixtures.')

    def quarter_turns():
        original = {(0,0),(0,1),(0,2),(1,2),(2,2)}
        current = set(original)
        first_rows = None
        for index in range(4):
            current = {(2-y,x) for x,y in current}
            if index == 0:
                first_rows = [''.join('1' if (x,y) in current else '0' for x in range(3)) for y in range(3)]
        return {'first_rotation_rows': first_rows, 'four_turns_restore': current == original}

    check('quarter-turn-topology', ['rotation-policy'],
          {'first_rotation_rows': ['111','100','100'], 'four_turns_restore': True}, quarter_turns,
          'Exact square-grid quarter turns only; arbitrary rotation, resampling and baked light direction remain unproven.')

    def normal_orientation():
        normals = [_normalize(v) for v in ((1,0,1),(-1,0,1),(0,1,1),(0,-1,1))]
        responses = [[round(max(0,sum(a*b for a,b in zip(n,light))),9) for light in normals] for n in normals]
        errors = []
        for normal in normals + [(0,0,1)]:
            encoded = [math.floor((value+1)*.5*255+.5) for value in normal]
            decoded = _normalize([2*value/255-1 for value in encoded])
            dot = min(1,max(-1,sum(a*b for a,b in zip(normal,decoded))))
            errors.append(math.degrees(math.acos(dot)))
        return {'responses': responses, 'maximum_8bit_angular_error_deg': round(max(errors),9)}

    check('normal-orientation', ['normal-direction'],
          {'responses': [[1,0,.5,.5],[0,1,.5,.5],[.5,.5,1,0],[.5,.5,0,1]],
           'maximum_8bit_angular_error_deg': '< 1 degree'}, normal_orientation,
          'Tests the declared x-right/y-up numeric convention and 8-bit quantization; no engine import or shader normal convention is certified.',
          lambda o: o['responses'] == [[1,0,.5,.5],[0,1,.5,.5],[.5,.5,1,0],[.5,.5,0,1]] and 0 <= o['maximum_8bit_angular_error_deg'] < 1)

    def visibility():
        def visible(segment):
            # General segment intersection for this noncollinear 2D fixture.
            def orient(a,b,c):
                return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
            light, receiver = (0,0), (4,0)
            a,b = segment
            crosses = orient(light,receiver,a)*orient(light,receiver,b) < 0 and orient(a,b,light)*orient(a,b,receiver) < 0
            return int(not crosses)
        return {'visibility': [visible(((2,-1),(2,1))), visible(((5,-1),(5,1)))], 'normal_term': [1,1]}

    check('shadow-occlusion', ['shadow-visibility'], {'visibility': [0,1], 'normal_term': [1,1]}, visibility,
          'A noncollinear segment-visibility fixture; soft shadows, polygon degeneracy and renderer shadow casting are not implemented.')

    def authored_shading():
        diffuse = (.2,.5,.8)
        neutral = [[round(d*(1+0*(light-.5)),9) for d in diffuse] for light in (0,.5,1)]
        low = [round(d*(1+.2*(0-.5)),9) for d in diffuse]
        high = [round(d*(1+.2*(1-.5)),9) for d in diffuse]
        return {'zero_strength': neutral, 'low_modulation': low, 'high_modulation': high}

    check('authored-shade-baseline', ['preserve-authored-shading'],
          {'zero_strength': [[.2,.5,.8],[.2,.5,.8],[.2,.5,.8]], 'low_modulation': [.18,.45,.72], 'high_modulation': [.22,.55,.88]},
          authored_shading, 'Illustrative linear scalar modulation only; preventing artistic double shading still needs rendered comparisons.')

    check('material-channel-isolation', ['material-channel-budget'], {'outputs': [.2,.6,.1,.5]},
          lambda: {'outputs': [round(.5*(.2+mask*.8)+emission,9) for emission in (.1,0) for mask in (0,1)]},
          'The formula is a reference fixture, not a platform material implementation or a validated 2.5D height pipeline.')

    def cluster_connectivity():
        points = {(1,1),(1,2),(2,1),(2,2),(5,1),(6,2),(1,6)}
        return {'four_neighbor_sizes': sorted(map(len,_components(points))),
                'eight_neighbor_sizes': sorted(map(len,_components(points,True)))}

    check('cluster-connectivity', ['semantic-clusters'],
          {'four_neighbor_sizes': [1,1,1,4], 'eight_neighbor_sizes': [1,2,4]}, cluster_connectivity,
          'Connectivity does not establish semantic importance; no singleton is automatically removed.')

    def cell_simulation():
        states,moves = _sand(1729)
        replay,replay_moves = _sand(1729)
        max_moves = max((max(Counter(move[0] for move in tick).values(),default=0) for tick in moves),default=0)
        bounded = all(max(abs(nx-x),abs(ny-y)) <= 1 for tick in moves for _,x,y,nx,ny in tick)
        counts = [len(state) for state in states]
        identities = all(set(state.values()) == {1,2,3} for state in states)
        return {'first_tick': sorted([particle,x,y] for (x,y),particle in states[1].items()),
                'particle_counts': counts, 'maximum_moves_per_id_per_tick': max_moves,
                'same_seed_same_states': states == replay and moves == replay_moves,
                'displacement_bound_holds': bounded, 'identities_preserved': identities}

    check('cell-conservation-determinism', ['deterministic-cell-update','cell-materials'],
          {'first_tick': [[1,3,2],[2,3,3],[3,4,2]], 'particle_counts': [3]*21,
           'maximum_moves_per_id_per_tick': 1, 'same_seed_same_states': True,
           'displacement_bound_holds': True, 'identities_preserved': True}, cell_simulation,
          'Three powder entities, one floor, one-cell movement and 20 serial ticks. Does not establish full fluid behavior, cross-chunk concurrency or Noita equivalence.')

    def destruction():
        points = {(x,y) for y in range(3) for x in (0,1,2,4,5,6)} | {(3,1)}
        before = _components(points)
        points.remove((3,1))
        after = _components(points)
        union = set().union(*after)
        overlap = sum(map(len,after))-len(union)
        return {'before_sizes': sorted(map(len,before)), 'after_sizes': sorted(map(len,after)),
                'union_size': len(union), 'overlap_size': overlap}

    check('destruction-components', ['destruction-topology'],
          {'before_sizes': [19], 'after_sizes': [9,9], 'union_size': 18, 'overlap_size': 0}, destruction,
          'Proves occupancy partition after one bridge removal. Contours, simplification, mass properties and rigid-body solver integration are not implemented.')

    def phased_regions():
        boxes = [(-1,-1,9,9),(7,-1,17,9),(15,-1,25,9)]
        conflicts = []
        for i in range(3):
            for j in range(i+1,3):
                a,b = boxes[i],boxes[j]
                if max(a[0],b[0]) < min(a[2],b[2]) and max(a[1],b[1]) < min(a[3],b[3]):
                    conflicts.append([i,j])
        return {'conflicting_pairs': conflicts}

    check('phase-write-domains', ['phased-write-ownership'], {'conflicting_pairs': [[0,1],[1,2]]}, phased_regions,
          'Proves three declared half-open rectangle intersections, not that an actual simulation respects those write bounds.')

    def sheet_roundtrip():
        sheet = Image.new('RGBA',(9,9))
        frames = [Image.new('RGBA',(3,3),color) for color in _PALETTE]
        origins = [(1,1),(5,1),(1,5),(5,5)]
        for frame,origin in zip(frames,origins):
            sheet.paste(frame,origin)
        extracted = [sheet.crop((x,y,x+3,y+3)) for x,y in origins]
        bad = sheet.crop((4,1,7,4))
        return {'roundtrip_matches': [a.tobytes()==b.tobytes() for a,b in zip(frames,extracted)],
                'wrong_spacing_detected': bad.tobytes()!=frames[1].tobytes()}

    check('sheet-offset-spacing', ['sheet-metadata'],
          {'roundtrip_matches': [True,True,True,True], 'wrong_spacing_detected': True}, sheet_roundtrip,
          'Fixed-grid RGBA extraction only; packed-atlas rotations and importer metadata need project-specific validation.')

    report = {'version': 1, 'status': 'pass' if all(item['status']=='pass' for item in checks) else 'fail',
              'scope': 'offline_reference_fixtures',
              'implementation_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'pillow_version': pillow_version, 'checks': checks, 'artifacts': artifacts,
              'limitations': ['No live PixelLab calls were made.',
                              'A passing reference fixture is not a provider capability, engine integration or visual-quality certification.',
                              'Unlisted knowledge methods retain their project/provider/visual POC recipes and have no execution result here.']}
    (output/'poc-report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    return report
