# Third-Party Licenses & Transparency Notice

> **Project:** `ellmos-ai/ellmos-voice-io`<br>
> **Audited:** 2026-09-12<br>
> **Repository License:** [MIT License](LICENSE)<br>
> **Architecture & Privacy:** 100% Local-First, Zero-Egress, Unprivileged User-Mode (`RunAsInvoker`), Deterministic Audio Hardware Lifecycle

---

## Executive Summary & Compliance Assurance

`ellmos-voice-io` is engineered under strict architectural and governance invariants: **100% Local-First, Zero-Egress by default, unprivileged user-mode execution (`RunAsInvoker`), and caller-owned audio hardware isolation**. The core Python package contains **zero direct runtime dependencies** (`dependencies = []`), eliminating unwanted third-party attack surfaces and ensuring zero background network or telemetry egress.

Optional external engine integrations (speech-to-text, text-to-speech, and wake-word detection) are strictly decoupled and loaded lazily on demand. Each optional dependency maintains explicit license tracking:

1. **Permissive Core & Ecosystem Compatibility:** The base package is 100% MIT-licensed. Core utilities, CLI status reporting, file dispatching, and wake-word listener contracts operate without requiring copyleft libraries.
2. **Explicit Copyleft Isolation (`piper-tts`):** The optional ONNX neural TTS engine `piper-tts` is licensed under **GPL-3.0-or-later**. Users who require strictly permissive environments can use `pyttsx3` (MPL-2.0) for system speech or omit TTS extras entirely. Installing the `all` or `tts-piper` extra is optional and isolated.
3. **No Bundled Model Weights or Audio Caches:** This repository does not ship, redistribute, or monetize proprietary or third-party voice models, neural weights, or acoustic datasets. Model acquisition remains the explicit responsibility and property of the consuming application.
4. **Deterministic Microphone Lifecycle:** Audio hardware is engaged exclusively during synchronous `WakeWordListener.listen()` executions and released immediately upon termination or cancellation.
5. **48h Security SLA:** Coordinated vulnerability response with guaranteed 48-hour response and 5-business-day triage commitment.

---

## Core Runtime Dependencies

The base distribution of `ellmos-voice-io` has **zero external runtime dependencies**:

```toml
dependencies = []
```

All standard status introspection, audio format path validations, stop-event coordinators, and CLI dispatchers rely exclusively on the Python standard library (`argparse`, `dataclasses`, `importlib`, `pathlib`, `re`, `subprocess`, `sys`, `threading`).

---

## Optional Engine Extras Matrix

Optional dependencies are partitioned into distinct extras under `[project.optional-dependencies]`:

| Optional Extra | Component | License | Declared Functional Scope | Upstream Source |
|:---|:---|:---:|:---|:---|
| `stt-whisper` | `openai-whisper` | MIT | Neural speech-to-text transcription | <https://github.com/openai/whisper> |
| `stt-vosk` | `vosk` | Apache-2.0 | Offline speech-to-text transcription | <https://github.com/alphacep/vosk-api> |
| `tts-pyttsx3` | `pyttsx3` | MPL-2.0 | System voice text-to-speech synthesis | <https://github.com/nateshmbhat/pyttsx3> |
| `tts-piper` | `piper-tts` | **GPL-3.0-or-later** | Local ONNX fast neural voice synthesis | <https://github.com/OHF-Voice/piper1-gpl> |
| `wakeword` | `openwakeword` | Apache-2.0 | Lightweight local wake-word evaluation | <https://github.com/dscripka/openWakeWord> |
| `wakeword` | `PyAudio` | MIT | PortAudio bindings for microphone streaming | <https://pypi.org/project/PyAudio/> |
| `wakeword` | `NumPy` | BSD-3-Clause | Numerical audio buffer manipulation | <https://github.com/numpy/numpy> |

---

## Optional System Utilities

| Tool | License | Trigger / Usage Boundary | Upstream Reference |
|:---|:---:|:---|:---|
| **FFmpeg Executable** | LGPL-2.1+ / GPL-2.0+ (build dependent) | Invoked via `subprocess` solely when a caller explicitly requests non-WAV output (`.mp3`, `.ogg`) | <https://ffmpeg.org/legal.html> |

FFmpeg is never bundled with `ellmos-voice-io`. It is discovered via the host's system `PATH` only when transcode operations are requested.

---

## Direct Development & Quality Assurance Tooling

All developer dependencies are pinned to standard permissive open-source licenses:

| Package | Version | License | Functional Scope |
|:---|:---:|:---:|:---|
| `build` | `>=1.2` | MIT / Apache-2.0 | PEP 517 build frontend |
| `pytest` | `>=8.0` | MIT | Test runner and assertion framework |
| `ruff` | `>=0.8` | MIT / Apache-2.0 | Static analysis and linter |
| `tomli` | `>=2.0` | MIT | TOML parser for Python 3.10 |
| `twine` | `>=5.0` | Apache-2.0 | Distribution artifact checker |

---

## Acoustic Models & Neural Weights Boundary

1. **Whisper Models:** Official OpenAI Whisper model checkpoints are released under the MIT license. `ellmos-voice-io` requires explicit `allow_model_download=True` or an existing offline model path; it never initiates silent background downloads.
2. **Vosk Acoustic Models:** Vosk models are typically released under Apache-2.0 or CC-BY licenses depending on the language pack chosen by the user.
3. **Piper Voice Models:** ONNX voice models for Piper are licensed independently by their respective creators (commonly MIT, Open Data Commons, or CC licenses).
4. **openWakeWord Models:** Default `.tflite` / `.onnx` models provided upstream by openWakeWord are distributed under the Apache-2.0 license.

---

## Verification & Audit Metadata

- **Audit Date:** 2026-09-12
- **Auditor:** ELLMOS AI Quality & Governance Pipeline
- **Methodology:** AST import analysis, PEP 621 manifest verification, transitive dependency inspection, and automated license-file contract test suites.
- **Fail-Closed Verification:** Automated test `test_license_files_metadata_contract` and `test_third_party_inventory_calls_out_piper_copyleft` in `tests/test_metadata.py` and `tests/test_public_readiness.py`.
