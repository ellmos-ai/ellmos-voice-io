# Security Policy / Sicherheitsrichtlinie

**[English](#english)** | **[Deutsch](#deutsch)**

---

<a name="english"></a>
## English

### Security & Privacy Invariants

`ellmos-voice-io` provides local-first audio input/output and wake-word primitives for LLMs, agent runtimes, and desktop applications. The module adheres to strict architectural security invariants:

1. **Local-First & Zero-Egress Invariant**:
   - Audio processing (STT and TTS) and wake-word evaluation occur locally on the host.
   - No background network connections, telemetry beacons, cloud analytics, or unauthorized audio uploads exist.
   - A named Whisper model may access the network only after the caller sets
     `allow_model_download=True`; otherwise a local model file is mandatory.
2. **Explicit Caller Authorization & Audio Retention**:
   - `ellmos-voice-io` does not manage persistent audio storage or background audio caches.
   - All input `.wav` files and generated audio files stay strictly at caller-provided file system paths.
3. **Hardware Boundary (Microphone Lifecycle)**:
   - Microphone access occurs exclusively during an explicit, synchronous invocation of `WakeWordListener.listen(on_wake, stop_event)`.
   - Audio hardware is never opened if `stop_event` is set prior to invocation.
   - When stopped or on runtime exceptions, audio input streams are deterministically terminated and closed.
4. **Lazy Engine Isolation**:
   - Optional heavy dependencies (such as Whisper, Vosk, pyttsx3, Piper, openWakeWord) are imported lazily on demand.
   - Unused engines are never loaded into process memory.
5. **Read-Only CLI Surface**:
   - `ellmos-voice-io status` is strictly read-only and outputs availability JSON without querying audio hardware or downloading models.

### Supported Versions

| Version | Supported | Notes |
|---------|-----------|-------|
| `0.2.x` | :white_check_mark: | Active development stream |

### Reporting a Vulnerability

If you discover a security vulnerability or privacy boundary leak in `ellmos-voice-io`:

1. **Do not open a public issue.**
2. Report the vulnerability privately via [GitHub Security Advisories](https://github.com/ellmos-ai/ellmos-voice-io/security/advisories/new) or by emailing `security@ellmos.ai` (cc: `support@lukasgeiger.com`, `lukas@open-bricks.org`).
3. **Response SLA**: Initial confirmation within **48 hours** and continuous triage updates.
4. Please provide a clear description of the vulnerability, reproduction steps, affected environment, and impact assessment.
5. Do not attach recordings, transcripts, credentials, model files, or other sensitive data unless a maintainer requests a safe transfer channel.

---

<a name="deutsch"></a>
## Deutsch

### Sicherheits- & Datenschutz-Invarianten

`ellmos-voice-io` stellt lokale Audio-Ein-/Ausgabe- und Wake-Word-Grundbausteine für LLMs, Agenten-Laufzeiten und Desktop-Anwendungen bereit. Das Modul erfüllt verbindliche architektonische Sicherheitsregeln:

1. **Local-First & Zero-Egress-Invariante**:
   - Audioverarbeitung (STT und TTS) sowie Wake-Word-Erkennung erfolgen vollständig lokal auf dem Host-System.
   - Es existieren keine Hintergrundnetzwerkverbindungen, Telemetrie-Dienste, Cloud-Analysen oder unautorisierte Audio-Uploads.
   - Ein benanntes Whisper-Modell darf erst nach ausdrücklichem
     `allow_model_download=True` auf das Netzwerk zugreifen; andernfalls ist
     eine lokale Modelldatei verpflichtend.
2. **Explizite Aufrufer-Autorisierung & Speicherung**:
   - `ellmos-voice-io` betreibt keine eigenständige persistente Speicherung oder Hintergrund-Audio-Caches.
   - Alle verarbeiteten `.wav`-Dateien und erzeugten Audiodateien verbleiben ausschließlich an den vom Aufrufer vorgegebenen Pfaden.
3. **Hardware-Grenze (Mikrofon-Lebenszyklus)**:
   - Der Zugriff auf das Mikrofon erfolgt ausschließlich während des synchronen Aufrufs von `WakeWordListener.listen(on_wake, stop_event)`.
   - Audiogeräte werden nicht geöffnet, wenn das `stop_event` bereits vor dem Aufruf gesetzt ist.
   - Bei Abbruch oder Laufzeitausnahmen werden Audiostreams deterministisch beendet und Hardware-Ressourcen freigegeben.
4. **Lazy Engine-Isolation**:
   - Optionale Bibliotheken (Whisper, Vosk, pyttsx3, Piper, openWakeWord) werden erst bei konkreter Anforderung geladen.
   - Nicht genutzte Engines belegen keinen Speicher im Host-Prozess.
5. **Rein lesende CLI-Schnittstelle**:
   - `ellmos-voice-io status` liest ausschließlich Verfügbarkeiten aus, ohne Audiogeräte zu initialisieren oder Modelle herunterzuladen.

### Unterstützte Versionen

| Version | Unterstützt | Anmerkungen |
|---------|-------------|-------------|
| `0.2.x` | :white_check_mark: | Aktiver Entwicklungszweig |

### Schwachstellen melden

Sollten Sie eine Sicherheitslücke oder eine Verletzung der Datenschutzgrenzen in `ellmos-voice-io` feststellen:

1. **Bitte erstellen Sie kein öffentliches Issue.**
2. Melden Sie die Schwachstelle vertraulich über [GitHub Security Advisories](https://github.com/ellmos-ai/ellmos-voice-io/security/advisories/new) oder per E-Mail an `security@ellmos.ai` (Kopie an: `support@lukasgeiger.com`, `lukas@open-bricks.org`).
3. **Reaktions-SLA**: Erstbestätigung innerhalb von **48 Stunden** und kontinuierliche Status-Updates.
4. Bitte fügen Sie eine Beschreibung, Reproduktionsschritte und eine Einschätzung der Auswirkungen bei.
5. Fügen Sie keine Aufnahmen, Transkripte, Zugangsdaten, Modelldateien oder anderen sensiblen Daten bei, solange kein sicherer Übertragungsweg mit den Maintainern vereinbart wurde.
