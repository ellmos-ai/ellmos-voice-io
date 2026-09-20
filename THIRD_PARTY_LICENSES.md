# Third-Party Licenses & Transparency Notice

> **Project:** `ellmos-ai/ellmos-voice-io`<br>
> **Audited:** 2026-09-20<br>
> **Repository License:** [MIT License](LICENSE)<br>
> **Architecture & Privacy:** 100% Local-First, Zero-Egress, Unprivileged User-Mode (`RunAsInvoker`), Deterministic Audio Hardware Lifecycle

---

## Executive Summary & Compliance Assurance

`ellmos-voice-io` is engineered under strict architectural and governance invariants: **100% Local-First, Zero-Egress by default, unprivileged user-mode execution (`RunAsInvoker`), and caller-owned audio hardware isolation**. The core Python package contains **zero direct runtime dependencies** (`dependencies = []`), eliminating unwanted third-party attack surfaces and ensuring zero background network or telemetry egress.

All optional external engine integrations (speech-to-text, text-to-speech, and wake-word detection) are strictly decoupled and loaded lazily on demand. Each optional dependency maintains explicit license tracking:

1. **100% Local-First & Zero-Egress (INV-LOCAL-01):** Operates entirely on local machines without outbound network connections, background telemetry, or cloud storage.
2. **Unprivileged User-Mode (`RunAsInvoker` / INV-SEC-02):** Executes safely in unprivileged user space without requiring root or administrator elevation.
3. **Explicit Model Download Consent (INV-CONSENT-03):** No implicit network connections or silent downloads for Whisper models; caller owns network policy.
4. **Deterministic Microphone Lifecycle (INV-MIC-04):** Audio capture hardware is engaged exclusively during synchronous `WakeWordListener.listen()` executions and released immediately upon termination or cancellation.
5. **Caller-Owned Audio Retention (INV-DATA-05):** Zero internal audio recordings, transcripts, or syntheses are stored in hidden caches or internal databases.
6. **Lazy Engine Isolation & Copyleft Isolation (INV-LAZY-06):** Core package is 100% MIT-licensed. The optional ONNX neural TTS engine `piper-tts` is licensed under **GPL-3.0-or-later**. Users requiring strictly permissive environments use `pyttsx3` (MPL-2.0) or native system voices. Installing `tts-piper` or `all` is purely optional and strictly isolated.
7. **Read-Only Inspection CLI (INV-CLI-07):** `ellmos-voice-io status` introspects environment availability via `importlib.util.find_spec` without opening audio hardware or downloading files.
8. **Cross-Platform Operating Parity (INV-PORT-08):** Consistent behavior across Windows, Linux, and macOS environments verified across Python 3.10-3.13.
9. **Cloud-Sync & Multi-Agent Defense (INV-SYNC-09):** Hardened against file locks and synchronization conflicts across distributed hosts.
10. **48h Security Response & Triage SLA (INV-SLA-10):** Guaranteed 48-hour response, 5-business-day triage, and 30-day remediation via canonical security channels (`security@open-bricks.org`, `security@ellmos.ai`).

---

## Level 1 Software Bill of Materials (SBOM)

| Component / Artifact | Type | Declared License | Upstream Source | Copyleft / AGPL | Role & Scope |
|:---|:---|:---|:---|:---|:---|
| **Python Standard Library** | Runtime Core | [PSFL-2.0](https://docs.python.org/3/license.html) | [python/cpython](https://github.com/python/cpython) | **None** (100% Permissive) | Audio dispatch, file I/O, process, threading, dataclasses, CLI |
| **openai-whisper** (optional) | STT Extra (`stt-whisper`) | [MIT](https://github.com/openai/whisper/blob/main/LICENSE) | [openai/whisper](https://github.com/openai/whisper) | **None** (Permissive) | Neural speech-to-text transcription engine |
| **vosk** (optional) | STT Extra (`stt-vosk`) | [Apache-2.0](https://github.com/alphacep/vosk-api/blob/master/COPYING) | [alphacep/vosk-api](https://github.com/alphacep/vosk-api) | **None** (Permissive) | Lightweight local offline speech-to-text engine |
| **pyttsx3** (optional) | TTS Extra (`tts-pyttsx3`) | [MPL-2.0](https://github.com/nateshmbhat/pyttsx3/blob/master/LICENSE) | [nateshmbhat/pyttsx3](https://github.com/nateshmbhat/pyttsx3) | Weak Copyleft (File-level) | System voice synthesis (SAPI5/NSSpeechSynthesizer/espeak) |
| **piper-tts** (optional) | TTS Extra (`tts-piper`) | [GPL-3.0-or-later](https://github.com/OHF-Voice/piper1-gpl/blob/master/LICENSE) | [OHF-Voice/piper1-gpl](https://github.com/OHF-Voice/piper1-gpl) | **Strong Copyleft** | Local fast neural ONNX voice synthesis (isolated optional extra) |
| **openwakeword** (optional) | Wake-Word Extra (`wakeword`) | [Apache-2.0](https://github.com/dscripka/openWakeWord/blob/main/LICENSE) | [dscripka/openWakeWord](https://github.com/dscripka/openWakeWord) | **None** (Permissive) | Local wake-word classification engine |
| **PyAudio** (optional) | Wake-Word Extra (`wakeword`) | [MIT](https://pypi.org/project/PyAudio/) | [bastibe/PyAudio](https://github.com/bastibe/PyAudio) | **None** (Permissive) | PortAudio bindings for microphone input streaming |
| **NumPy** (optional) | Wake-Word Extra (`wakeword`) | [BSD-3-Clause](https://github.com/numpy/numpy/blob/main/LICENSE.txt) | [numpy/numpy](https://github.com/numpy/numpy) | **None** (Permissive) | Fast numerical audio buffer processing |
| **pytest** | Development / Test | [MIT](https://github.com/pytest-dev/pytest/blob/main/LICENSE) | [pytest-dev/pytest](https://github.com/pytest-dev/pytest) | **None** (Permissive) | Test execution and contract verification runner |
| **ruff** | Development / QA | [MIT / Apache-2.0](https://github.com/astral-sh/ruff/blob/main/LICENSE-MIT) | [astral-sh/ruff](https://github.com/astral-sh/ruff) | **None** (Permissive) | Static linting and bytecode formatting gate |
| **setuptools** | Build Backend | [MIT](https://github.com/pypa/setuptools/blob/main/LICENSE) | [pypa/setuptools](https://github.com/pypa/setuptools) | **None** (Permissive) | PEP 517 / PEP 621 packaging build backend |
| **tomli** (Python < 3.11) | Development / Test | [MIT](https://github.com/hukkin/tomli/blob/master/LICENSE) | [hukkin/tomli](https://github.com/hukkin/tomli) | **None** (Permissive) | Python 3.10 TOML parsing compatibility fallback |

---

## Zero-Runtime-Dependency & Zero-Copyleft Isolation Guarantee

The base distribution of `ellmos-voice-io` guarantees:
- **Zero-Runtime-Dependency Guarantee**: The core package has **zero external runtime dependencies** (`dependencies = []` in `pyproject.toml`). All status introspection, path validation, stop-event coordination, and CLI dispatchers rely exclusively on the Python standard library (`argparse`, `dataclasses`, `importlib`, `pathlib`, `re`, `subprocess`, `sys`, `threading`).
- **Zero-Copyleft Base Wheel Guarantee**: 0% GPL, 0% AGPL, and 0% copyleft in the core runtime distribution. The base distribution is 100% MIT-licensed.
- **Strict Optional Copyleft Isolation (`piper-tts`)**: The optional ONNX neural TTS engine `piper-tts` is licensed under **GPL-3.0-or-later**. Users requiring strictly permissive environments can use `pyttsx3` (MPL-2.0) or omit TTS extras entirely. Installing the `all` or `tts-piper` extra is optional and decoupled.
- **Unprivileged User-Mode Execution (`RunAsInvoker`)**: Never requires administrative elevation, UAC prompts, or root filesystem writes.
- **Zero Model Redistribution**: No neural weights, voice checkpoints, or audio caches are bundled in this distribution.

---

## Invariant Cross-Reference Matrix

| Invariant ID | Name & Semantic Contract | Verification Mechanism & Implementation Component |
|:---|:---|:---|
| **INV-LOCAL-01** | 100% Local-First & Zero-Egress | `src/ellmos_voice_io/service.py`, `tests/test_metadata.py::test_documentation_hygiene` |
| **INV-SEC-02** | Unprivileged User-Mode (`RunAsInvoker`) | `src/ellmos_voice_io/cli.py`, `tests/test_metadata.py::test_governance_invariants_table` |
| **INV-CONSENT-03** | Explicit Model Download Consent | `src/ellmos_voice_io/stt.py`, `tests/test_service.py::test_whisper_named_model_requires_explicit_download_opt_in` |
| **INV-MIC-04** | Deterministic Microphone Hardware Lifecycle | `src/ellmos_voice_io/wakeword.py`, `tests/test_service.py::test_wakeword_repeated_hits_callback_contract_and_cleanup` |
| **INV-DATA-05** | Caller-Owned Audio Retention | `src/ellmos_voice_io/tts.py`, `src/ellmos_voice_io/stt.py` (direct caller file paths) |
| **INV-LAZY-06** | Lazy Engine & Copyleft Isolation | `src/ellmos_voice_io/stt.py`, `src/ellmos_voice_io/tts.py`, `tests/test_service.py::test_optional_engines_stay_lazy_during_construction` |
| **INV-CLI-07** | Read-Only Environment Inspection CLI | `src/ellmos_voice_io/cli.py`, `tests/test_service.py::test_status_cli_is_read_only` |
| **INV-PORT-08** | Cross-Platform Operating Parity | `.github/workflows/ci.yml`, `tests/test_public_readiness.py::test_ci_declares_all_supported_platforms` |
| **INV-SYNC-09** | Cloud-Sync & Multi-Agent Defense | `.gitignore`, `tests/test_metadata.py::test_gitignore_multihost_and_lock_patterns` |
| **INV-SLA-10** | Dual Security Response & Triage SLA | `SECURITY.md`, `tests/test_metadata.py::test_security_sla_and_contacts` |

---

## Optional System Utilities

| Tool | License | Trigger / Usage Boundary | Upstream Reference |
|:---|:---:|:---|:---|
| **FFmpeg Executable** | LGPL-2.1+ / GPL-2.0+ (build dependent) | Invoked via `subprocess` solely when a caller explicitly requests non-WAV output (`.mp3`, `.ogg`) | <https://ffmpeg.org/legal.html> |

FFmpeg is never bundled with `ellmos-voice-io`. It is discovered via the host's system `PATH` only when transcode operations are requested.

---

## Acoustic Models & Neural Weights Boundary

1. **Whisper Models:** Official OpenAI Whisper model checkpoints are released under the MIT license. `ellmos-voice-io` requires explicit `allow_model_download=True` or an existing offline model path; it never initiates silent background downloads.
2. **Vosk Acoustic Models:** Vosk models are typically released under Apache-2.0 or CC-BY licenses depending on the language pack chosen by the user.
3. **Piper Voice Models:** ONNX voice models for Piper are licensed independently by their respective creators (commonly MIT, Open Data Commons, or CC licenses).
4. **openWakeWord Models:** Default `.tflite` / `.onnx` models provided upstream by openWakeWord are distributed under the Apache-2.0 license.

---

## Full License Texts (Excerpts & Notices)

### 1. Python Software Foundation License Version 2 (PSFL-2.0)
Python standard library modules are used under the PSF License Agreement.
Copyright (c) 2001-2026 Python Software Foundation. All rights reserved.

### 2. MIT License (MIT)
Used by `ellmos-voice-io`, `openai-whisper`, `PyAudio`, `pytest`, `ruff`, and `setuptools`.

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### 3. Apache License Version 2.0 (Apache-2.0)
Used by `vosk`, `openwakeword`, and dual-license option for `ruff`.
Licensed under the Apache License, Version 2.0. You may obtain a copy of the License at `http://www.apache.org/licenses/LICENSE-2.0`.

### 4. Mozilla Public License 2.0 (MPL-2.0)
Used by `pyttsx3`.
Covered Software is provided under the terms of the Mozilla Public License, v. 2.0. You may obtain a copy of the license at `https://www.mozilla.org/MPL/2.0/`.

### 5. BSD-3-Clause License (BSD-3-Clause)
Used by `NumPy`.
Copyright (c) 2005-2026, NumPy Developers. All rights reserved.

### 6. GNU General Public License v3.0 or later (GPL-3.0-or-later)
Used by the optional `piper-tts` engine.
This engine is strictly optional and isolated within the `tts-piper` extra. Consuming applications that require strictly permissive environments must omit the `tts-piper` extra.

---

## Verification & Audit Metadata

- **Audit Date:** 2026-09-20
- **Auditor:** ELLMOS AI Quality & Governance Pipeline
- **Methodology:** AST import analysis, PEP 621 manifest verification, transitive dependency inspection, and automated license-file contract test suites.
- **Fail-Closed Verification:** Automated tests in `tests/test_metadata.py` and `tests/test_public_readiness.py`.
