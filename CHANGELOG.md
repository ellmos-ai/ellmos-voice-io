# Changelog

## [0.1.2] - 2026-08-16

- Technical hygiene and linter standardization (Pfad A):
  - Integrated `[tool.ruff]` and `[tool.ruff.lint]` configuration in `pyproject.toml` (`target-version = "py310"`, `line-length = 120`, `E402`/`E501` ignore).
  - Added automated metadata & manifest contract test suite `tests/test_metadata.py` (verifying version parity across `pyproject.toml`, `ellmos-module.v2.json`, and `__init__.__version__`, required fields, and module exports).
  - Synchronized test badges and last-checked timestamps in `README.md`, `README_de.md`, and `llms.txt` (20/20 passed in 0.14s).
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
