# Changelog

## [0.2.0] - 2026-08-25 (public release)

- Repository visibility changed to public (owner decision F7=B): the GitHub
  repository `ellmos-ai/ellmos-voice-io` moved from private to public.
- Replaced the development history with a single clean baseline commit
  reflecting the reviewed, gate-passed tree (see `RELEASE_GATE.md`). The prior
  17-commit development history is preserved locally (backup branch and git
  bundle, not published) for internal reference; it is not part of the public
  repository.

## [0.2.0] - 2026-08-25

- Repository Hygiene, CI Hardening, PEP 621 Metadata & Contract Parity (Pfad A):
  - Hardened GitHub Actions CI workflow (`.github/workflows/ci.yml`) with automated concurrency control (`cancel-in-progress: true`).
  - Extended `pyproject.toml` with PEP 621 ecosystem URLs (`Parent Organization`, `Umbrella Ecosystem`, `Changelog`) and normalized pytest pythonpath to include repository root for isolated test discovery.
  - Hardened bilingual security policy (`SECURITY.md`) with explicit 48h response SLA and official security contacts (`security@ellmos.ai`, `support@lukasgeiger.com`, `lukas@open-bricks.org`).
  - Expanded `.gitignore` with sync conflict patterns (`*.sync-conflict-*`, `*.conflict`, `*-CONFLIT-*`) and development caches (`.ruff_cache/`, `.mypy_cache/`, `*.tmp`).
  - Expanded automated contract test suite in `tests/test_metadata.py` to 40 passed tests with verifications for CI concurrency, PEP 621 URLs, security SLA/contacts, and gitignore hygiene patterns.
  - Synchronized Shields.io test badges in `README.md` / `README_de.md` and machine-readable `llms.txt` context to 40 passed tests and 2026-08-25 timestamp.

## [0.2.0] - 2026-08-21

- Enforced the no-implicit-network contract for Whisper: named models require
  `allow_model_download=True`; local model files remain the offline default.
- Added deterministic regression coverage for Whisper download consent and
  local-model routing without loading a real model or accessing the network.
- Added cross-platform CI, reproducible package checks, public contribution and
  conduct documents, third-party license inventory, AI deployment note, and a
  fail-closed release gate.
- Corrected installation guidance: the package is not published to PyPI and is
  installed from a trusted checkout until a separately approved release exists.
- Added the project banner and synchronized English/German privacy, package,
  provenance, and release documentation.
- Removed a host-specific development path from the current public surface;
  historical commits remain documented as a low-risk publication decision.
- Aligned `ellmos-module.v2.json` with the strict canonical schema: the explicit
  Whisper download path is represented as optional network access, unpublished
  package metadata is not advertised as an installable registry release, and
  unsupported manifest fields were removed.
- Pinned the current Node-24 GitHub Actions to immutable commit SHAs, added
  Python 3.10 to the Windows/macOS/Linux matrix, supplied the `tomllib`
  compatibility dependency for that minimum version, and added regressions
  for the declared support range and movable workflow action references.
- Added the shared MODULES pre-release status contract and its exact minimum
  ignore set; the common Final Gate Check now passes 10/10 while external
  publication remains owner-locked.

## [0.1.2] - 2026-08-20

- Discoverability, Sibling Ecosystem & Metadata Parity Check (Pfad B):
  - Synchronized package version `0.1.2` across `pyproject.toml`, `ellmos-module.v2.json`, `src/ellmos_voice_io/__init__.py`, `llms.txt`, and Shields.io badges.
  - Added bilingual security policy `SECURITY.md` defining local-first, zero-telemetry invariants, explicit caller-owned retention, microphone hardware lifecycle isolation, and vulnerability disclosure.
  - Added comprehensive bilingual Ecosystem & Sibling Tools cross-linking matrix (`README.md` and `README_de.md`) connecting `ellmos-ai`, `dev-bricks`, `doc-bricks`, and `open-bricks` suites.
  - Expanded automated test suite in `tests/test_metadata.py` to 24 tests covering version parity, manifest contracts, package exports, security policy, sibling matrix integrity, and doc hygiene.
  - Synchronized `llms.txt` index timestamp to 2026-08-20, test count (24 passed), and reference catalog.

## [0.1.1] - 2026-08-16

- Technical hygiene and linter standardization (Pfad A):
  - Integrated `[tool.ruff]` and `[tool.ruff.lint]` configuration in `pyproject.toml` (`target-version = "py310"`, `line-length = 120`, `E402`/`E501` ignore).
  - Added initial metadata contract test suite in `tests/test_metadata.py`.
  - Verified static hygiene (`ruff check .` 0 errors, `python -m compileall` 0 errors).

## [0.1.1] - 2026-08-14

- Discoverability, documentation, and SEO enhancements:
  - Added comprehensive [`llms.txt`](llms.txt) machine-readable index for LLM agents, tools, and RAG pipelines.
  - Added Shields.io status badges (Python 3.10+, MIT license, 17 pytest tests passed, local-first privacy, llms.txt, ellmos-ai org, open-bricks ecosystem) to `README.md` and `README_de.md`.
  - Added bilingual navigation switcher (`[English](README.md)` | `[Deutsch](README_de.md)`) and GFM tips callout for `llms.txt`.
  - Added interactive Mermaid system architecture diagram visualizing facade layer, lazy optional engine bindings, and privacy boundaries.
  - Added structured engine capabilities matrix and complete Python API examples.
  - Executed test suite (17 passed in 0.90s) and static hygiene verification (`ruff check .`).

## [0.1.0] - 2026-08-01

- Initial independent extraction of an earlier internal Voice Service core.
- Added optional Whisper/Vosk STT, pyttsx3/Piper TTS, and openWakeWord integration.
- Added explicit privacy boundaries, Python API, CLI status surface, and tests.
