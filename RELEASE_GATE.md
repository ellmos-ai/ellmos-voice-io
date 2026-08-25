# Release Gate: ellmos-voice-io

## Status

```text
+------------------------------------------+
|                                          |
|          STATUS: PUBLISHED                |
|                                          |
+------------------------------------------+
```

The GitHub repository is **public** as of 2026-08-25 (owner decision F7=B,
recorded in ticket T-20260824-289138658). The development history was replaced
with a single clean baseline commit at the same time (see "History boundary"
below); the prior history is preserved locally and was never pushed. The
package remains **not published** to PyPI; a PyPI/registry upload still
requires a separate, explicit repository-owner decision.

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
| 10 | External release authority | PASS | Owner approved public visibility 2026-08-25 (F7=B); PyPI/registry upload remains a separate, still-locked decision |

## Registry and naming snapshot

Checked 2026-08-21, rechecked 2026-08-25 immediately before the visibility
change:

- GitHub exact search (unauthenticated `repositories?q=ellmos-voice-io+in:name`):
  0 results (the repository was still private at check time, so it does not
  appear in unauthenticated search either).
- PyPI exact project endpoint (`ellmos-voice-io` and `ellmos_voice_io`): 404;
  the package is not published.
- npm exact package lookup: 404; broader npm search shows no colliding
  `ellmos-voice-io` package (only unrelated results and our own `ellmos-*`
  MCP packages).

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
credential, recording, model, or internal report. The prior 17-commit
development history (all commits used a GitHub noreply author address) is
documented here for the record without reproducing the literal path: it
retained a generic Windows local-development clone path (a
`repos/ellmos-voice-io` checkout under a personal development root,
introduced in one commit and later removed from the tracked tree) and a
reference to an earlier internal system name ("BACH") in the original commit
message and README prose of the first commit; a later commit generalized the
README wording but the commit message itself is immutable history.

On 2026-08-25, following owner decision F7=B (ticket T-20260824-289138658),
that history was replaced: a single clean orphan-branch commit reflecting the
reviewed, gate-passed tree became the new `main`. The full prior history is
preserved **locally only** — backup branch
`backup/pre-history-replace-20260825` and git bundle
`ellmos-voice-io-full-history-20260825.bundle` (17 commits, verified complete)
— and was never pushed to the now-public remote.

## Evidence boundary

Unit and package tests use deterministic doubles. They do not prove that
Whisper, Vosk, Piper, pyttsx3, openWakeWord, a microphone, a system voice, or
FFmpeg works on a real target host. They also do not authorize model downloads,
audio capture, publication, or credentials.

Reviewed: 2026-08-21

Decision: PUBLISHED 2026-08-25 (owner decision F7=B, ticket T-20260824-289138658; history replaced, backup preserved locally, not pushed)
