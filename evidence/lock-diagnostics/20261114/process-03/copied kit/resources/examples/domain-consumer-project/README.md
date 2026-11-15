# Animation and terrain diagnostic project

This project is an executable starting point for the shipped
[sprite animation](../consumer-execution/sprite-animation/README.md) and
[tile neighborhood](../consumer-execution/tile-neighborhood/README.md) profiles.
The twenty PNGs are authored diagnostic geometry. They are not PixelLab outputs
or evidence of generated art quality. [BRIEF.md](BRIEF.md) supplies the project's
visual intent and separate mechanical and visual criteria.

The animation source declares uneven durations, per-frame pivots, a planted
anchor, a looping idle and a clamped one-shot. The terrain source declares this
project's NW/NE/SE/SW binary corner order and two neighborhoods; the mixed map
contains all sixteen tile IDs. Those conventions belong to this project.

For an existing current family, map every member output to these actual asset
paths in the appropriate `consumer-execute` config. The two domains use separate
family candidates and configurations. Follow the profile README and
[execution contract](../../spec/consumer-execution.md). Both profiles provide an
interactive destination as well as isolated headless capture, independent checks
and NF-06 observation import. The operation writes evidence without accepting art.

Maintainers can prepare disposable diagnostic state through
`evaluations.domain_consumer_case.project(Path(destination))` using the selected
development environment. The helper measures real PNG dimensions and alpha,
accepts only those mechanical member criteria, then retains an unreviewed family
with open visual continuity and destination requirements. `defects=True` adds two
controlled pixel faults before state preparation. It does not change metadata or
renderer expectations; mechanical rendering should still pass. This helper is
evaluation preparation, not a production authoring shortcut.

For a useful production revision, start with [CF-09-ASSIGNMENT.md](CF-09-ASSIGNMENT.md).
Keep original art, failed observations, source intent and unrelated valid members.
Replacing these diagnostic pixels with art does not itself demonstrate acceptance.
