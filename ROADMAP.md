# ellmos-voice-io Roadmap

## Verified preparation — 2026-08-21

`ellmos-voice-io` remains a small, LLM-neutral runtime module for explicit
local speech-to-text, text-to-speech, and wake-word operations. Optional engines
stay lazy; the base package has no storage, telemetry, background service, or
implicit network activity.

### Completed gates

| Former task | Gate | Verified result |
|---:|---|---|
| 1877 | PACKAGE-PREFLIGHT | Reproducible sdist/wheel, clean-install CLI smoke, tests, Ruff, compileall, Twine, and archive inspection |
| 1878 | ENGINE-CONTRACTS | Hardware-, model-, and network-free test doubles cover Vosk, Whisper, pyttsx3, Piper routing, conversion, and failure paths |
| 1879 | PLATFORM-CI | Checked-in CI covers Windows, macOS, and Linux on Python 3.10, 3.11, and 3.12 without audio hardware |
| 1881 | WAKEWORD-LIFECYCLE | Cancellation, repeated hits, callback/read/open failures, and deterministic stream cleanup are specified and tested |

The Whisper path now fails closed: a caller supplies a local model file or opts
in explicitly to a named-model download. The read-only `status` command never
opens hardware or downloads models.

### Remaining external gates

| Gate | Owner | Condition |
|---|---|---|
| Repository visibility | Repository owner | Explicit decision after reviewing `RELEASE_GATE.md` and the local publication report |
| PyPI publication | Repository owner | Separate registry approval, trusted-publishing setup, package-name review, and uploaded-artifact readback |
| Optional-engine platform evidence | Maintainers | Real engine/model/hardware checks on each claimed platform; unit tests do not claim this evidence |
| Model and voice licensing | Distributors | Review every selected model/voice license in addition to the direct dependency inventory |
| Commercial name clearance | Repository owner | Official similarity search before commercialization or package registration |

No release, upload, visibility change, credential operation, microphone access,
or model download is authorized by this roadmap.
