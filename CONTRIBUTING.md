# Contributing to ellmos-voice-io / Mitwirken an ellmos-voice-io

Welcome! We welcome contributions to `ellmos-voice-io`. To maintain stability, deterministic audio hardware handling, privacy-first zero-egress boundaries, and compliance across multi-host environments, all contributions must adhere to the quality standards and operational invariants defined below.

---

## English

### 1. General Principles & Quality Gates
1. **Local-First & Air-Gapped (`INV-LOCAL-01`)**: All core library and CLI logic must operate strictly offline. Never introduce background telemetry, analytics, remote sockets, or cloud storage.
2. **User-Mode Non-Elevation (`INV-SEC-02` / `RunAsInvoker`)**: All CLI commands, status introspection, audio processing, and wake-word listeners execute strictly in unprivileged user space without requiring root or administrative UAC elevation.
3. **Explicit Model Download Consent (`INV-CONSENT-03`)**: Never trigger automatic or silent model downloads over the network. Network activity is permitted only when the caller explicitly passes `allow_model_download=True`.
4. **Deterministic Microphone Hardware Lifecycle (`INV-MIC-04`)**: Microphone capture streams are opened exclusively inside synchronous `WakeWordListener.listen()` executions and must be reliably released in `finally` blocks upon termination or cancellation.
5. **Caller-Owned Audio Retention (`INV-DATA-05`)**: Zero persistence or caching of captured audio or transcription results within the library.
6. **Lazy Engine & Copyleft Isolation (`INV-LAZY-06`)**: Core package is 100% MIT-licensed with zero runtime dependencies. Optional engines (`vosk`, `whisper`, `pyttsx3`, `piper-tts`, `openwakeword`) are imported lazily on demand.
7. **Read-Only Inspection CLI (`INV-CLI-07`)**: `ellmos-voice-io status` outputs structured availability JSON without opening hardware or writing state.
8. **Cross-Platform Operating Parity (`INV-PORT-08`)**: Consistent behavior across Windows, Linux, and macOS across Python 3.10-3.13.
9. **Multi-Host & Lock Defense (`INV-SYNC-09`)**: Hardened against file locks, temporary artifacts, and synchronization conflicts across distributed hosts.
10. **48h Security SLA (`INV-SLA-10`)**: 48h response SLA, 5-business-day triage, and 30-day remediation.
11. **Version Freeze Discipline (`T-20260920-167562623`)**: Version 0.2.1 is strictly frozen across all manifests. Do not bump the version string. Document all advancements under `## [Unreleased]` in `CHANGELOG.md`.
12. **Bilingual Documentation Parity**: Maintain synchronized structural and navigational parity across `README.md` and `README_de.md` (18-point dual anchors `sec-01` through `sec-18`).

### 2. Local Development Workflow
```bash
# Install package with development dependencies
python -m pip install -e ".[dev]"

# Run comprehensive test suite
python -X utf8 -m pytest -ra -v

# Run linter
python -m ruff check .

# Check bytecode compilation
python -m compileall -q src tests

# Check whitespace and git diff cleanliness
git diff --check
```

### 3. Submission Protocol
- Open an issue for behavioral discussions before large refactoring.
- Keep credentials, private tokens, and test recordings strictly outside the repository.
- Ensure all 10 governance invariants (`INV-LOCAL-01` to `INV-SLA-10`) remain VERIFIED.

---

## Deutsch

### 1. Grundsätze & Qualitäts-Tore
1. **Local-First & Zero-Egress (`INV-LOCAL-01`)**: Sämtliche Kernbibliotheken und CLI-Abläufe arbeiten zu 100% offline ohne Telemetrie, Sockets oder externe Datenübertragung.
2. **User-Mode Non-Elevation (`INV-SEC-02` / `RunAsInvoker`)**: CLI-Befehle, Status-Introspektion und Audio-Verarbeitung laufen strikt im unprivilegierten Standard-Benutzerkontext ohne UAC-Elevation.
3. **Ausdrückliche Modell-Download-Zustimmung (`INV-CONSENT-03`)**: Keine impliziten oder stillen Modell-Downloads über das Netzwerk. Netzwerkaktivität erfordert die explizite Option `allow_model_download=True`.
4. **Deterministischer Mikrofon-Lebenszyklus (`INV-MIC-04`)**: Audio-Streams werden nur innerhalb von synchronen `WakeWordListener.listen()`-Aufrufen geöffnet und in `finally`-Blöcken deterministisch freigegeben.
5. **Aufrufer-eigene Audio-Haltung (`INV-DATA-05`)**: Keine interne Speicherung oder Zwischenspeicherung von Audiodaten oder Transkripten.
6. **Lazy Engine & Copyleft-Isolation (`INV-LAZY-06`)**: Basis-Wheel ist 100% MIT-lizenziert ohne Laufzeitabhängigkeiten. Optionale Engines werden ausschließlich bedarfsweise (lazy) geladen.
7. **Rein lesende CLI-Introspektion (`INV-CLI-07`)**: `ellmos-voice-io status` liefert strukturierte JSON-Ausgaben ohne Hardware- oder Netzwerkzugriff.
8. **Plattformübergreifende Laufzeitparität (`INV-PORT-08`)**: Einheitliches Verhalten unter Windows, Linux und macOS über Python 3.10-3.13.
9. **Multi-Host- & Lock-Schutz (`INV-SYNC-09`)**: Gehärtet gegen Lock-Dateien und Synchronisationskonflikte.
10. **48h Sicherheits-SLA (`INV-SLA-10`)**: 48h Reaktions-SLA und koordinierte Offenlegung.
11. **Strikte Versions-Freeze-Disziplin (`T-20260920-167562623`)**: Version 0.2.1 bleibt in allen Manifesten eingefroren. Keine Versionserhöhung vornehmen; alle Änderungen unter `## [Unreleased]` in `CHANGELOG.md` festhalten.
12. **Zweisprachige Dokumentationsparität**: `README.md` und `README_de.md` müssen strukturgleich und mit synchronen 18-Punkte-HTML-Ankern (`sec-01` bis `sec-18`) gepflegt werden.

### 2. Lokaler Entwicklungsablauf
```bash
# Entwicklungsumgebung einrichten
python -m pip install -e ".[dev]"

# Vollständige Testsuite ausführen
python -X utf8 -m pytest -ra -v

# Linter-Prüfung
python -m ruff check .

# Bytecode-Kompilierung
python -m compileall -q src tests

# Diff- und Whitespace-Prüfung
git diff --check
```

### 3. Einreichung
- Vor größeren Eingriffen ein Issue zur Abstimmung anlegen.
- Zugangsdaten, API-Schlüssel und Test-Audios niemals ins Repository committen.
- Alle 10 Invarianten (`INV-LOCAL-01` bis `INV-SLA-10`) müssen erfüllt bleiben.
