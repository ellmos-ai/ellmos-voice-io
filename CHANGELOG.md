# Changelog

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
