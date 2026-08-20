# Changelog

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

- Initial independent extraction of the BACH Voice Service core.
- Added optional Whisper/Vosk STT, pyttsx3/Piper TTS, and openWakeWord integration.
- Added explicit privacy boundaries, Python API, CLI status surface, and tests.
