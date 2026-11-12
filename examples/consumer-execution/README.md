# Executable destination profiles

Use [`consumer-execute` / `pixl_consumer_execute`](../../spec/consumer-execution.md)
to capture a current family in its actual declared consumer. The operation copies
a fixed renderer, checks source and destination identity, captures an isolated
browser, checks its pixels and imports an NF-06 observation. Review that observation
separately; execution does not accept art or change production state.

| Consumer contract | Profile | Observations |
| --- | --- | --- |
| Queue state and full/compact views | [queue-motion-v1](../../spec/consumer-execution.md#operation-inputs) | State mapping, observed playback, reduced-motion holds and switching |
| Authored sprite clips | [sprite-animation-v1](sprite-animation/README.md) | Uneven duration, crop/pivot/anchor placement, looping and one-shot playback |
| Binary corner terrain | [tile-neighborhood-v1](tile-neighborhood/README.md) | Actual corner-to-tile calls and pixels in explicit neighborhoods |

Each profile uses a closed configuration and explicit module exports. Choose it
from the actual project's contract. The [diagnostic domain project](../domain-consumer-project/README.md)
provides runnable animation and terrain source/assets with project-specific
criteria. The [robot direction renderer](../delegation/renderer/README.md) remains
a separate CF-10 consumer; it is not a fixed `consumer-execute` profile.

Captures retain exact source, files, config and renderer alongside execution and
cleanup receipts. Use a fresh output directory after any failure. These are trusted
local consumer modules in isolated processes, not an operating-system sandbox.
