# Handoff — robot family baseline review

State: `.pixl/state.px`, PX2 revision 2, hash `e0121ba9c1025994ad34bbccb1464647217b8043c726d05170e8aa6f144a3f62`.
Start a cold session with `pixl_workflow` on that file, then read `inspection/visual-review-r1.md`.

## Decision (`d_baseline`)

**candidate.png is not ready to be the robot family baseline.** It matches the mechanical contract
but is reference.png minus two identity features: the whole left antenna and the whole right eye.
Baseline defects are inherited by every later member and would become the yardstick for family
continuity checks, so this is rejected rather than accepted with a note.

| Criterion | Domain | Verdict |
| --- | --- | --- |
| `q_mech` — 32x32, reference palette, binary alpha, one component | mechanical | pass (`v_mech`) |
| `q_identity` — both antennae, both eyes, symmetric | visual | **fail** (`v_identity`) |
| `q_baseline` — no unexplained feature loss a family would inherit | other | **fail** (`v_baseline`) |

## Next step (`handoff` → `review_sample`, still active)

Produce a revised sample that keeps everything currently correct and restores the two lost features,
nominate it on the same output `sample_f`, and re-evaluate it against the same three saved criteria.
Revision 1 stays retained as `sample_x1`; the new candidate cannot inherit its passing mechanical
verdict. Family production starts only after this sample is accepted.

Target for the revision, in reference.png coordinates:

- Left antenna: 24 pixels of `#25354A` in the block x 7–10, y 3–8, mirroring the surviving right antenna.
- Right eye: 12 pixels of `#F4DDA2` in the block x 18–20, y 14–17, mirroring the surviving left eye.

## Still unresolved (blocks family planning, not the revision)

- `roster` — which robots the family contains, and in what poses or variants.
- `destination` — no target engine, import route or display scale, so no engine criterion is declared
  and no import behaviour has been verified or claimed.

## Files

- `assets/robot_sample_r1.png` — retained byte-identical snapshot of the reviewed candidate.
- `inspection/` — the 12x enlargements, the difference map, and the two retained observation files
  bound as evidence (`e_mech`, `e_visual`).
- `sources/assignment.md` — the assignment as given.
- `.pixl/build_plan.py`, `.pixl/build_results.py` — how the two committed revisions were authored.
