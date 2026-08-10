# ellmos-voice-io Roadmap

## Recheck 2026-08-02

`ellmos-voice-io` is a small, LLM-neutral runtime module for explicit local
speech-to-text, text-to-speech, and wake-word operations. The package keeps
engines optional and lazy, has no storage or telemetry boundary, and exposes a
read-only `status` CLI.

Intake baseline: canonical clone `C:\_Local_DEV\repos\ellmos-voice-io`, branch
`main`, HEAD `317dadb7930ddb40dcaeec11a6adc4b85b6bd5a7`, tracking `origin/main`
at `https://github.com/ellmos-ai/ellmos-voice-io.git`; no foreign lock was
present. The manifest remains `status=development` and `visibility=private`.

The source manifest declares Windows, macOS, and Linux, but the repository has
no CI workflow or checked-in build/readback record. Existing tests cover the
facade, validation, missing-file and CLI guard cases; optional-engine paths,
real platform evidence, and release provenance are not yet established by
the checked-in controls. No task was executed during this recheck.

## Prioritized next work

| TaskPLAN | Gate | Priority | Effort | Scope | Next verifiable result |
|---:|---|---|---|---|---|
| 1877 | PACKAGE-PREFLIGHT | high | medium | local | Reproducible sdist/wheel, clean install, compileall, tests, CLI and hash readback |
| 1878 | ENGINE-CONTRACTS | medium | medium | local | Deterministic, hardware/model/network-free contracts for optional engines |
| 1879 | PLATFORM-CI | medium | large | local | Separate Windows/macOS/Linux CI evidence or explicit runner/dependency blockers |
| 1880 | RELEASE-PROVENANCE | high | special | local | User decision and provenance for development/private status versus Pip distribution |
| 1881 | WAKEWORD-LIFECYCLE | medium | medium | local | Defined and isolated callback, cancellation, repeated-hit, and cleanup contract |

Task details, sources, acceptance criteria, dependencies, and boundaries are
recorded in TASKPLAN. Release, upload, registry writes, credentials, and
microphone permission remain outside this writer pass.

