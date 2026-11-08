# PX-PKG-001 — production dependency installation

Implemented 2026-11-07. Mandatory dependencies are Pillow and jsonschema. Mypy, Ruff, Sourcery, setuptools, typing stubs and tiktoken moved intact to the dev group with coverage; tokenizer measurement also remains available through the existing benchmark extra. The lockfile preserves the resolved versions. The plugin builder derives requirements from the same production dependency list.

[Recorded installation](20261107/result.json) built checkout → sdist → wheel, installed into a new unseeded environment, and exercised PLAR/reference handoff, source retention/cold recovery, state/knowledge/capability operations, all reference POCs, provider-state and family-delivery probes, plus the copied plugin. These probes use local fixtures; they do not certify generated art or native agent behavior.

Installed distributions: pixl-agent, Pillow, jsonschema, attrs, jsonschema-specifications, referencing and rpds-py. No lint/type/build/coverage/tokenizer tools were installed in that runtime environment. The verifier now checks this boundary on every distribution run; it no longer borrows the development interpreter's site-packages. Build/install logs are retained beside the result. Maintainer tools remain available via the default dev sync. No global installation was changed.

The first offline lock refresh lacked registry metadata; the normal online refresh succeeded without changing package versions. An initial Ruff string-concatenation diagnostic in the verifier was corrected before installation validation. Final repository verification is linked from the current overall TODO and evidence/test-results.json.

## Required A–E review

- **A — Improvement:** users install only dependencies used by the runtime; maintainers retain their complete tooling.
- **B — Hosts:** this changes Python installation, not Claude/Codex profile discovery or their official PixelLab connection. Both kit and installed runtime are exercised from a different project directory.
- **C — Quality:** less installation burden helps reach the asset workflow; it supplies no evidence of better artistic decisions.
- **D — Other projects:** a clean environment can use the wheel or relocated plugin without this checkout's development dependencies.
- **E — Responsibilities:** packaging supplies runtime dependencies; the profile/skills continue to own artistic work and workflow; MCP/API execution boundaries are unchanged.

Scope: the recorded Windows/Python 3.14 environment. The declared Python 3.11+ range and other operating systems were not exhaustively installed here. PX-PKG-001 is complete for its defined dependency separation and installation checks; overall product acceptance remains open.
