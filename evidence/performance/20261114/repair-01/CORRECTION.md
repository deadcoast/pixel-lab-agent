The first focused run passed 45 of 46 tests; the new complete-context assertion
used the connected plan record as its focus and incorrectly expected that wire
closure to contain a later criterion source. Plan metadata strings do not create
UDL reference edges. The authoring operation itself, CLI/MCP parity, binary drift
refusals, remote-source behavior and scoped Ruff passed.

The retained test source and original logs remain unchanged. The corrected test
requests complete context for `next.motion.output`, whose criterion actually
references the binary source. This changes the assertion's requested closure,
not the runtime or saved-state semantics. A separate repair-02 run records the
result; no earlier failure is relabeled as a pass.
