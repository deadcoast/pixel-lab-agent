# Literal coverage diagnostic against native01

This is a synthetic mechanical diagnostic using current repository source. It is
not another native qualification or a source-grounded review of the caller's
claims. [The receipt](run-01/receipt.json) records **18/18 checks passing**.

The exact `CALLER-RESULT-LITERAL-RECONCILIATION.json` bytes came from the retained
`native-01/project.zip`, member SHA-256
`7b033ec23f1307ab3083e8061fb5456a61fc389085b8b00ac36158d0f03229e3`.
The checker inventories the whole `/remaining_questions` and `/next_action`
subtrees: **22 leaves**, including all five later RQ3 fields. See
[the inventory](run-01/consumer/inventory.json) and
[exact RQ3 values](run-01/rq3-exact-inventory.json).

- [Omitting RQ3's unlocks row](run-01/consumer/omitted-row-check.json) yields
  `coverage_incomplete`, CLI exit 1, and the precise missing pointer
  `/remaining_questions/2/unlocks`.
- [The deliberately wrong complete review](run-01/consumer/wrong-but-complete-check.json)
  copies all saved values and intentionally classifies even operational claims as
  metadata. That violates production review guidance, but mechanically covers all
  22 leaves. It receives `coverage_complete`, CLI exit 0, and still
  **`semantic_verdict: not_assessed`**. No source or carrier authority is certified.
- The original native01 tree, current source runtime tree, copied result, and
  review inputs retain their bytes and modification times. Before/after manifests
  are retained beside the receipt. No native02 inputs were changed.

The helper and exact subprocess commands are retained. To rerun without replacing
evidence, choose a new run name:

```powershell
.venv/Scripts/python.exe -B evidence/skill-handoff/literal-reconciliation-20261116/tool-diagnostic-01/run_diagnostic.py.txt --run run-02
```

Relocated-kit execution is separately covered by the passing scoped tests under
`../tool-development-01/checks-02/`; this diagnostic does not substitute for that
test or for independent semantic review.
