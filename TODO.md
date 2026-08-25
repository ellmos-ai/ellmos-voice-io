# Pre-Release TODO: ellmos-voice-io

**Audit date:** 2026-08-21

**Target repository:** `ellmos-ai/ellmos-voice-io`

**Scope:** private public-readiness preparation; no release authorization

## Blockers

No current-tree blocker remains in the shared MODULES Final Gate Check.

## Owner decisions before public release

- [x] Decide whether to retain the existing repository history or publish from a
  sanitized replacement history. Earlier commits retain a generic local
  development root and an earlier internal system name. **Decided 2026-08-25
  (owner decision F7=B, ticket T-20260824-289138658): replace.** History
  replaced with a single clean orphan-branch commit; prior 17-commit history
  preserved locally only (backup branch + git bundle, never pushed). See
  `RELEASE_GATE.md`, "History boundary".
- [x] Explicitly authorize the visibility change, tag, GitHub Release, and any
  package-registry publication as separate actions. **The visibility change is
  authorized and executed 2026-08-25 (F7=B).** No tag, GitHub Release, or
  package-registry publication has been authorized or performed; those remain
  separate, still-open decisions.
- [ ] Complete an official name-similarity check before commercialization or
  external package registration. Availability recheck done 2026-08-25 (GitHub,
  PyPI, npm: no collision found) as part of the public-visibility change; this
  is still only an availability indicator, not trademark clearance, and the
  item stays open until an actual commercialization/registration step needs it.

## Evidence still required for production claims

- [ ] Validate each advertised optional engine on intended target systems.
- [ ] Validate microphone capture, system voices, playback, models, and FFmpeg
  separately; deterministic tests intentionally do not exercise hardware or
  download models.
- [ ] Review model and voice licenses for every concrete distribution. Piper is
  GPL-3.0-or-later and remains optional and unbundled.

## Status

| Category | Status | Notes |
|---|---|---|
| Secrets | READY | No secret patterns in the tracked tree |
| Private data (PII) | READY | No direct personal address or host-specific user path in the current tree |
| `.gitignore` | READY | Shared minimum plus audio, lock, build, and internal-report exclusions |
| Language (English) | READY | English README is primary; German companion is synchronized |
| BACH internals | READY | No BACH-internal document is tracked |
| Database files | READY | No database is tracked; `*.db` and `data/` are excluded |
| README.md | READY | Purpose, installation, boundaries, and examples are documented |
| LICENSE | READY | MIT project license present; third-party terms are inventoried separately |
| **Overall technical gate** | **PUBLISHED** | Public since 2026-08-25 (F7=B); see `RELEASE_GATE.md` |

**Gate check exit code:** `0` after the 2026-08-21 remediation; re-scanned clean with
`repo_privacy_gate.py --repo` on 2026-08-25 immediately before the visibility change.
