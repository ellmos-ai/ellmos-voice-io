# Changelog

## Unreleased

- Maintenance verification (2026-08-10): 6 pytest tests passed, `python -m compileall src` passed, and the read-only `status` surface reported Vosk and pyttsx3 available while wake-word support remained unavailable; no microphone, model download, or network action was started.
- Modernized PEP 621 license metadata to avoid current setuptools deprecation warnings.

## 0.1.0 - 2026-08-01

- Initial independent extraction of the BACH Voice Service core.
- Added optional Whisper/Vosk STT, pyttsx3/Piper TTS, and openWakeWord integration.
- Added explicit privacy boundaries, Python API, CLI status surface, and tests.
