# Release Gate: ellmos-voice-io

## Status

```text
+------------------------------------------+
|                                          |
|          STATUS: LOCKED                  |
|                                          |
+------------------------------------------+
```

The GitHub repository remains **PRIVATE** and the package is **not published**
to PyPI. A visibility change, tag, GitHub Release, or registry upload requires
an explicit repository-owner decision after this private preparation.

## Technical checklist

| # | Check | Current result | Boundary |
|---:|---|---|---|
| 1 | Ignore and release contents | PASS | No audio, models, credentials, caches, locks, or internal reports are tracked or present in the built archives |
| 2 | English/German documentation | PASS | Code blocks, versions, privacy, and release state match; prose is intentionally translated |
| 3 | MIT project license | PASS | Covers this repository only |
| 4 | Third-party inventory | PASS | Piper GPL and separate model/voice licenses are explicit |
| 5 | No implicit network | PASS | Whisper requires a local model or explicit download opt-in; three focused regressions pass |
| 6 | Deterministic tests | PASS (36/36) | No hardware, model, voice, playback, or network use |
| 7 | Package build/install | PASS | Two byte-identical builds, Twine validation, archive scan, and clean-install CLI smoke pass |
| 8 | Cross-platform CI definition | PASS | Windows, macOS, Linux; Python 3.10, 3.11, and 3.12 |
| 9 | Current-tree privacy scan | PASS | Matches are policy/test vocabulary only; history is assessed separately |
| 10 | External release authority | LOCKED | Owner approval remains mandatory |

## Registry and naming snapshot

Checked 2026-08-21:

- GitHub exact search: only the private `ellmos-ai/ellmos-voice-io` repository.
- PyPI exact project endpoint: 404; the package is not published.
- npm exact package lookup: 404; no package found.

These checks are availability indicators, not trademark clearance. An official
similarity search remains required before commercialization or package
registration.

## Reproducible artifact evidence

Two independent builds used `SOURCE_DATE_EPOCH=1787270400`, followed by the
checked-in sdist normalizer. Both copies were byte-identical:

| Artifact | SHA-256 |
|---|---|
| `ellmos_voice_io-0.2.0-py3-none-any.whl` | `3e2048823ea0fe15db5629d4d04edb272ea44c66b6f0f7f8f8ff3fde9119aad0` |
| `ellmos_voice_io-0.2.0.tar.gz` | `ae4d6b24b1acc0906b6c5c5af3b0d87f157f099a9f1366b86f54cd7dd507cdf3` |

Twine accepted all four artifacts. A clean environment installed the wheel
without optional dependencies, imported version `0.2.0`, and ran the read-only
`ellmos-voice-io status` command without hardware or network access. Archive
inspection found no audio, model, credential, lock, cache, or bytecode files.

## History boundary

The current tree contains no host-specific user path, direct maintainer email,
credential, recording, model, or internal report. All 12 existing commits use
a GitHub noreply author address. Earlier commits retain a generic host-local
development root and an earlier internal system name in documentation history.
No automatic history rewrite was performed; keeping or replacing that history
remains a repository-owner publication decision.

## Evidence boundary

Unit and package tests use deterministic doubles. They do not prove that
Whisper, Vosk, Piper, pyttsx3, openWakeWord, a microphone, a system voice, or
FFmpeg works on a real target host. They also do not authorize model downloads,
audio capture, publication, or credentials.

Reviewed: 2026-08-21

Decision: LOCKED
