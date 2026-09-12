<p align="center">
  <img src="docs/assets/banner.png" alt="ellmos-voice-io: lokaler Mikrofon-, Sprachverarbeitungs- und Lautsprecherfluss" width="900">
</p>

# ellmos-voice-io

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-0.2.1-blue.svg)](CHANGELOG.md)
[![CI Status](https://img.shields.io/badge/CI-Multi--OS%20Actions-success?logo=github-actions&logoColor=white)](.github/workflows/ci.yml)
[![Code Style: Ruff](https://img.shields.io/badge/Code%20Style-Ruff-000000.svg?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![Tests](https://img.shields.io/badge/Tests-56%20bestanden-brightgreen?logo=pytest&logoColor=white)](tests/)
[![Platform](https://img.shields.io/badge/Plattform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](pyproject.toml)
[![Privacy: Zero-Egress](https://img.shields.io/badge/Datenschutz-100%25%20Offline%20%7C%20Zero--Egress-success)](README_de.md#9-datenschutz-und-hardware-grenzen)
[![Security: Local-First](https://img.shields.io/badge/Sicherheit-Local--First%20%7C%20RunAsInvoker-blue)](SECURITY.md)
[![Security SLA](https://img.shields.io/badge/Sicherheits--SLA-48h%20Antwort-blue.svg)](SECURITY.md)
[![License: MIT](https://img.shields.io/badge/Lizenz-MIT-green.svg)](LICENSE)
[![Org](https://img.shields.io/badge/Org-ellmos--ai-8A2BE2)](https://github.com/ellmos-ai)
[![Umbrella](https://img.shields.io/badge/Umbrella-open--bricks-indigo)](https://github.com/open-bricks)
[![llms.txt](https://img.shields.io/badge/llms.txt-verf%C3%BCgbar-0055ff?logo=markdown)](llms.txt)

**[English](README.md)** | **[Deutsch](README_de.md)**

> [!TIP]
> **Maschinenlesbare Dokumentation:** Ein [`llms.txt`](llms.txt)-Index steht für KI-Agenten, LLMs und automatisierte RAG-Pipelines bereit.

### Schnellnavigation

- [1. Kurzfassung](#1-kurzfassung)
- [2. Systemarchitektur & Komponentenfluss](#2-systemarchitektur--komponentenfluss)
- [3. Audio-Lebenszyklus & Ereignisfluss](#3-audio-lebenszyklus--ereignisfluss)
- [4. Sicherheitsmodell & Governance-Invarianten](#4-sicherheitsmodell--governance-invarianten)
- [5. Umfang & Unterstützte Engines](#5-umfang--unterstützte-engines)
- [6. Installation & Umgebungseinrichtung](#6-installation--umgebungseinrichtung)
- [7. Rein lesende CLI-Bedienung](#7-rein-lesende-cli-bedienung)
- [8. Python-API-Integration](#8-python-api-integration)
- [9. Datenschutz und Hardware-Grenzen](#9-datenschutz-und-hardware-grenzen)
- [10. Zielgruppen & Auffindbarkeit](#10-zielgruppen--auffindbarkeit)
- [11. Drittanbieter-Lizenzen & Abhängigkeits-Audits](#11-drittanbieter-lizenzen--abhängigkeits-audits)
- [12. Ökosystem & Geschwister-Werkzeuge](#12-ökosystem--geschwister-werkzeuge)
- [13. Entwicklungsstatus & Roadmap](#13-entwicklungsstatus--roadmap)
- [14. Provenienz & Historien-Grenze](#14-provenienz--historien-grenze)
- [15. Sicherheitsrichtlinie & Meldewege](#15-sicherheitsrichtlinie--meldewege)
- [16. Lizenz, Urheberrecht & Englische Dokumentation](README.md)

---

## 1. Kurzfassung

`ellmos-voice-io` stellt lokale Speech-to-Text-, Text-to-Speech- und Wake-Word-Hilfen für LLM-Systeme, Agenten-Laufzeiten und Desktop-Anwendungen bereit.

`ellmos-voice-io` ist ein kleines, LLM-neutrales Laufzeitmodul. Es startet keinen Server, speichert keine Aufnahmen, liefert keine Stimmmodelle aus und wählt keinen Cloud-Provider. Aufrufer wählen optionale lokale Engines ausdrücklich und verantworten Mikrofonberechtigungen, Modelldownloads, Aufbewahrung und jede Netzwerkintegration.

| Wenn Sie folgendes tun möchten... | Öffnen Sie... |
|---|---|
| Komponentenarchitektur einsehen | [2. Systemarchitektur & Komponentenfluss](#2-systemarchitektur--komponentenfluss) |
| Audio- und Wake-Word-Ausführung verfolgen | [3. Audio-Lebenszyklus & Ereignisfluss](#3-audio-lebenszyklus--ereignisfluss) |
| Sicherheitsinvarianten & SLA prüfen | [4. Sicherheitsmodell & Governance-Invarianten](#4-sicherheitsmodell--governance-invarianten) |
| Paket & optionale Extras installieren | [6. Installation & Umgebungseinrichtung](#6-installation--umgebungseinrichtung) |
| Engine-Verfügbarkeit per CLI abfragen | [7. Rein lesende CLI-Bedienung](#7-rein-lesende-cli-bedienung) |
| Python STT/TTS/Wake-Word anbinden | [8. Python-API-Integration](#8-python-api-integration) |
| Zielgruppen & Anwendungsfälle einsehen | [10. Zielgruppen & Auffindbarkeit](#10-zielgruppen--auffindbarkeit) |
| Drittanbieter-Lizenzen & Audits prüfen | [11. Drittanbieter-Lizenzen & Abhängigkeits-Audits](#11-drittanbieter-lizenzen--abhängigkeits-audits) |
| Multi-Agenten-Geschwister erkunden | [12. Ökosystem & Geschwister-Werkzeuge](#12-ökosystem--geschwister-werkzeuge) |
| KI-/LLM-Indexdatei lesen | [llms.txt](llms.txt) |
| Den englischen Leitfaden lesen | [README.md](README.md) |

---

## 2. Systemarchitektur & Komponentenfluss

```mermaid
graph TD
    UserApp["Caller / LLM Application / MCP Adapter"]
    
    subgraph FacadeLayer ["ellmos-voice-io Runtime"]
        VoiceIO["VoiceIO (Unified Facade)"]
        CLI["CLI (ellmos-voice-io status)"]
        STT["SpeechToText"]
        TTS["TextToSpeech"]
        WakeWord["WakeWordListener"]
    end
    
    subgraph OptionalEngines ["Optional Lazy Engines"]
        Vosk["Vosk (Local Offline STT)"]
        Whisper["Whisper (Neural STT)"]
        Pyttsx3["pyttsx3 (System TTS)"]
        Piper["Piper (ONNX Neural TTS)"]
        OpenWakeWord["openWakeWord (Local Mic)"]
    end
    
    subgraph PrivacyBoundary ["Privacy & Hardware Boundary"]
        Mic["Microphone (Caller-Authorized)"]
        AudioFiles["Local WAV / MP3 / OGG Files"]
        ZeroNet["Zero Telemetry / Zero Cloud Storage"]
    end

    UserApp --> VoiceIO
    UserApp --> CLI
    VoiceIO --> STT
    VoiceIO --> TTS
    VoiceIO --> WakeWord
    
    STT -.-> Vosk
    STT -.-> Whisper
    TTS -.-> Pyttsx3
    TTS -.-> Piper
    WakeWord -.-> OpenWakeWord
    
    Vosk --> AudioFiles
    Whisper --> AudioFiles
    Pyttsx3 --> AudioFiles
    Piper --> AudioFiles
    OpenWakeWord --> Mic
    
    style PrivacyBoundary fill:#f4f9f4,stroke:#4CAF50,stroke-width:2px;
    style FacadeLayer fill:#f0f4f8,stroke:#2196F3,stroke-width:2px;
```

---

## 3. Audio-Lebenszyklus & Ereignisfluss

```mermaid
sequenceDiagram
    autonumber
    actor Caller as Caller / LLM App / Agent
    participant Facade as VoiceIO Facade
    participant STT as SpeechToText Engine
    participant TTS as TextToSpeech Engine
    participant Wake as WakeWordListener
    participant Audio as Local Audio / Speaker / Mic

    rect rgb(240, 245, 255)
    note right of Caller: 1. Speech-to-Text (STT) - Local File Processing
    Caller->>Facade: transcribe_file("clip.wav", engine="vosk")
    Facade->>STT: Route to lazy local engine
    STT->>Audio: Read local .wav bytes (Zero Network)
    Audio-->>STT: Audio PCM buffer
    STT-->>Caller: Transcribed text string
    end

    rect rgb(245, 255, 240)
    note right of Caller: 2. Text-to-Speech (TTS) - Local Synthesis
    Caller->>Facade: speak_to_file("Alert", "out.wav", engine="piper")
    Facade->>TTS: Synthesize via local model / system voice
    TTS->>Audio: Write output audio file or stream to speaker
    Audio-->>Caller: Synthesis complete (Zero Egress)
    end

    rect rgb(255, 250, 240)
    note right of Caller: 3. Wake-Word Detection - Caller-Owned Lifecycle
    Caller->>Wake: listen(on_wake=callback, stop_event=event)
    loop Synchronous Chunk Read
        Wake->>Audio: Read mic frame (Active Stream)
        Audio-->>Wake: 16-bit PCM chunk
        Wake->>Wake: Predict wake-word probability
        opt Probability >= Threshold
            Wake->>Caller: invoke on_wake() callback
        end
    end
    Caller->>Wake: set stop_event
    Wake->>Audio: Deterministically terminate & close stream
    Wake-->>Caller: Return cleanly
    end
```

---

## 4. Sicherheitsmodell & Governance-Invarianten

Die folgenden 10 Invarianten regeln alle Laufzeitoperationen, CLI-Einstiegspunkte und Engine-Bindungen von `ellmos-voice-io`:

| # | Invariante | Garantie | Durchsetzungs-Mechanismus |
|---|---|---|---|
| 1 | **100% Local-First & Zero-Egress** | STT-, TTS- und Wake-Word-Operationen laufen vollständig offline ohne Telemetrie oder Cloud-Dienste. | Reine lokale Verarbeitung; keine ausgehenden Netzwerkverbindungen im Standardbetrieb. |
| 2 | **Non-Elevation (RunAsInvoker)** | Modul arbeitet strikt im unprivilegierten Benutzermodus ohne Administrator- oder Root-Rechte. | Läuft im Benutzermodus; nutzt reguläre Betriebssystem-APIs und Audiogeräte-Treiber. |
| 3 | **Explizite Modelldownload-Zustimmung** | Keine impliziten Netzwerkzugriffe oder unbemerkte Downloads für Whisper-Modelle. | Verpflichtender `allow_model_download=True`-Parameter; andernfalls zwingend lokale Modelldatei. |
| 4 | **Deterministischer Mikrofon-Lebenszyklus** | Mikrofonhardware wird ausschließlich während aktiver synchroner `listen()`-Aufrufe belegt. | Deterministisches Schließen der Streams in `finally`-Blöcken; gesetztes Stop-Event beendet sofort. |
| 5 | **Aufrufer-eigene Audiospeicherung** | Keine persistenten Aufnahmen, Transkripte oder Synthesen in versteckten Caches oder Datenbanken. | Dateien werden ausschließlich an vom Aufrufer vorgegebenen Pfaden gelesen und geschrieben. |
| 6 | **Lazy Engine-Isolation** | Schwere optionale Abhängigkeiten (Whisper, Vosk, pyttsx3, Piper, openWakeWord) laden nur bei Bedarf. | Verzögerte Imports in Engine-Klassen; ungenutzte Bibliotheken belegen keinen Arbeitsspeicher. |
| 7 | **Rein lesende CLI-Inspektion** | `ellmos-voice-io status` liefert strukturiertes JSON ohne Hardware-Aktivierung oder Downloads. | Reine Modul-Introspektion über `importlib.util.find_spec` ohne Nebeneffekte auf Audiogeräte. |
| 8 | **Plattformübergreifende Betriebsparität** | Einheitliches Verhalten unter Windows, Linux und macOS. | Multi-OS GitHub Actions CI-Matrix für Python 3.10, 3.11 und 3.12. |
| 9 | **Cloud-Sync- & Multi-Agenten-Schutz** | Schutz vor Synchronisationskonflikten und konkurrierenden Datei-Locks über mehrere Hosts. | `.gitignore` filtert `LOCK.*`, `*.lock`, `*.sync-conflict-*`, `*.conflict` und temporäre Dateien. |
| 10 | **48h Sicherheits-SLA & Koordinierte Meldung** | Verbindliche Reaktionszeiten bei Sicherheits- und Datenschutzmeldungen. | In `SECURITY.md` verankertes 48h-Bestätigungs-SLA, 5-Werktage-Triage und Multi-Inbox-Meldeweg. |

---

## 5. Umfang & Unterstützte Engines

- **Dateibasiertes STT**: Speech-to-Text über optionales Whisper oder Vosk.
- **Lautsprecher- & Datei-TTS**: Text-to-Speech auf Lautsprecher oder in Dateien über optionales pyttsx3 oder Piper.
- **Lokales Wake-Word**: Lokale Mikrofon-Wake-Word-Erkennung in Echtzeit über optionales openWakeWord.
- **Stabile Python-API & Read-Only CLI**: Statusabfrage per `status`-CLI für Skills, MCP-Adapter und Desktop-Apps.

| Fähigkeit | Unterstützte Engines | Eingabe / Ausgabe | Kernmerkmal |
|---|---|---|---|
| **Speech-to-Text** | `vosk`, `whisper` | `.wav`-Datei $\to$ Text | Vollständig offline mit lokalem Modell |
| **Text-to-Speech** | `pyttsx3`, `piper` | Text $\to$ `.wav` / `.mp3` / `.ogg` / Lautsprecher | Systemstimmen oder neuronale ONNX-Synthese |
| **Wake-Word** | `openwakeword` | Mikrofonstream $\to$ Callback | Synchroner, aufrufer-kontrollierter Stopp |

Das Modul ersetzt bewusst keine Audio-Workstations wie KlangpultLight oder USBPodcastStudio. Deren Aufnahme-, Schnitt-, Streaming- und Transkript-Workflows bleiben anwendungsspezifische Konsumenten dieser engeren Fähigkeit.

---

## 6. Installation & Umgebungseinrichtung

Das Paket ist noch nicht auf PyPI veröffentlicht. Bis zu einer vom Eigentümer
freigegebenen Veröffentlichung erfolgt die Installation ausschließlich aus
einem vertrauenswürdigen lokalen Checkout:

```bash
# Minimal base package (no optional heavy dependencies)
python -m pip install .

# Install with specific optional extras
python -m pip install ".[stt-vosk,tts-pyttsx3]"

# Development and verification toolchain
python -m pip install -e ".[dev]"
```

Das Extra `all` installiert auch `piper-tts`, dessen aktuelle Distribution
unter GPL-3.0-or-later steht. Prüfe vor einer Weitergabe
[`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md) und die Lizenzen der
ausgewählten Stimmen und Modelldateien.

---

## 7. Rein lesende CLI-Bedienung

Engine-Verfügbarkeit sicher prüfen ohne Hardware-Initialisierung oder externe Netzanfragen:

```bash
ellmos-voice-io status
```

Ausgabe:
```json
{
  "stt_available": true,
  "stt_engine": "vosk",
  "tts_available": true,
  "tts_engine": "pyttsx3",
  "wakeword_available": false,
  "wakeword_engine": "Install the wakeword extra to access microphone-based wake words."
}
```

---

## 8. Python-API-Integration

### Speech-to-Text (STT)

```python
from ellmos_voice_io import SpeechToText

# Using Vosk with an explicit local model path
stt = SpeechToText(engine="vosk", model_path="/path/to/vosk-model-de")
transcript = stt.transcribe_file("input_voice.wav")
print(f"Transcribed: {transcript}")

# Using Whisper with an explicit local model file (no network access)
stt_whisper = SpeechToText(engine="whisper", model_path="/path/to/base.pt")
transcript_whisper = stt_whisper.transcribe_file("meeting_clip.wav", language="en")

# A named model may download only after explicit opt-in
stt_download = SpeechToText(
    engine="whisper",
    model_size="base",
    allow_model_download=True,
)
```

### Text-to-Speech (TTS)

```python
from ellmos_voice_io import TextToSpeech

tts = TextToSpeech(engine="pyttsx3", rate=160)

# Speak directly to system default speakers
tts.speak("Processing complete.")

# Export synthesis directly to an audio file (.wav, .mp3, .ogg)
tts.speak_to_file("Notification sound generated.", "output/alert.wav")
```

### Wake-Word Listener

```python
import threading
from ellmos_voice_io import WakeWordListener

def on_wake():
    print("Wake word detected! Activating assistant...")

stop_event = threading.Event()
listener = WakeWordListener(threshold=0.6)

# Blocks until stop_event is set; handles cleanup automatically
listener.listen(on_wake=on_wake, stop_event=stop_event)
```

---

## 9. Datenschutz und Hardware-Grenzen

- **Audio, Transkripte und Ausgabedateien bleiben am vom Aufrufer bestimmten Ort.**
- **Kein Datenbankzugriff, keine Telemetrie, kein Konto, kein Hintergrunddienst, kein impliziter Upload.**
- **Mikrofonzugriff erfolgt ausschließlich während aktivem `WakeWordListener.listen()`.**
- **Kein impliziter Whisper-Download**: Verwende eine lokale Modelldatei oder
  erlaube den Download ausdrücklich mit `allow_model_download=True`; Netzwerk-
  und Modelllizenzregeln verbleiben dann beim Aufrufer.
- **Rein lesende CLI**: `status` fordert keine Berechtigungen an und lädt keine Modelle herunter.

### Wake-Word-Lebenszyklus

`WakeWordListener.listen(on_wake, stop_event)` ist synchron und aufrufer-kontrolliert:
- Ein vorab gesetztes `stop_event` kehrt sofort zurück, ohne Audiogeräte zu öffnen.
- Jeder Audio-Chunk mit einer Vorhersage $\ge$ Schwellenwert löst den Callback genau einmal aus. Entprellung verbleibt beim Aufrufer.
- Das `stop_event` wird vor jedem Leseschritt geprüft. Modell-, Stream- und Lese-Ausnahmen werden nach geordnetem Beenden des Audiostreams sicher weitergereicht.

---

## 10. Zielgruppen & Auffindbarkeit

`ellmos-voice-io` wurde gezielt für vier Entwickler- und Betreiber-Zielgruppen entworfen:

1. **Autonome lokale KI-Agenten-Entwickler & Schwarm-Operatoren:** Leichtgewichtige, latenzarme Sprachtranskription, Audiosynthese und freihändige Wake-Word-Erkennung für Agenten-Frameworks (Claude Code, Antigravity, Codex, Kimi, n8n) ohne speicherhungrige Hintergrund-Daemons oder wiederkehrende Cloud-API-Gebühren.
2. **Datenschutzbewusste Desktop-Anwendungsentwickler:** Entwicklung von Desktop-Software mit PySide6, PyQt, Tkinter oder Electron-Bridges mit lokaler Diktatfunktion oder System-Sprachausgabe, die zu 100 % offline arbeitet und strenge Datenschutzauflagen erfüllt.
3. **Edge- & Embedded-KI-Ingenieure:** Betrieb lokaler Wake-Word-Erkennung und Sprachsynthese auf Raspberry Pi, Mini-PCs oder luftdicht abgeschotteten Industrie-Terminals mit deterministischem Hardware-Lebenszyklus und sofortiger Ressourcenfreigabe.
4. **Sicherheits- & Compliance-Verantwortliche in Unternehmen:** Gewährleistung vollständiger Audio-Isolation, Verhinderung von Datenabflüssen (`INV-LOCAL-01`), Ausführung ohne erhöhte Privilegien (`INV-PRIV-02`) und vollkommene Transparenz über Drittanbieter-Lizenzen und Modellquellen.

Ausführliche Suchbegriffe, zweisprachige Auffindbarkeitsmatrizen und Wettbewerbsanalysen finden sich in [`MARKETING-LOG.txt`](MARKETING-LOG.txt).

---

## 11. Drittanbieter-Lizenzen & Abhängigkeits-Audits

Das Basis-Wheel von `ellmos-voice-io` besitzt **keinerlei externe Laufzeitabhängigkeiten** (`dependencies = []`), wodurch Risiken in der Lieferkette vollständig vermieden werden.

Optionale Sprach- und Wake-Word-Engines sind in modulare Extras ausgelagert:
- **Basis-Laufzeit & Fassade:** MIT-Lizenz (100 % permissiv).
- **Vosk STT (`stt-vosk`):** Apache-2.0-Lizenz.
- **OpenAI Whisper STT (`stt-whisper`):** MIT-Lizenz (ausdrückliches Netzwerk-Opt-in durch den Aufrufer).
- **pyttsx3 TTS (`tts-pyttsx3`):** MPL-2.0-Lizenz (nutzt native Betriebssystem-Stimmen).
- **openWakeWord (`wakeword`):** Apache-2.0-Lizenz.
- **PyAudio & NumPy (`wakeword`):** MIT / BSD-3-Clause.
- **Piper TTS (`tts-piper`):** **GPL-3.0-or-later** (isoliertes Copyleft-Modul; rein optional und niemals im Basispaket enthalten).

Vollständige Abhängigkeits-Audits, Systemwerkzeug-Grenzen (FFmpeg) und Richtlinien zu Modellgewichten sind in [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md) dokumentiert.

---

## 12. Ökosystem & Geschwister-Werkzeuge

Teil der [ellmos-ai](https://github.com/ellmos-ai) Multi-Agenten-Infrastruktur und des übergeordneten [open-bricks](https://github.com/open-bricks) Open-Source-Software-Ökosystems:

| Werkzeug | Organisation | Beschreibung |
|---|---|---|
| [ellmos-core](https://github.com/ellmos-ai/ellmos-core) | ellmos-ai | Modulare KI-Laufzeit, Aufgaben-Dispatching & Agenten-Zustandssubstrat |
| [ellmos-scheduler](https://github.com/ellmos-ai/ellmos-scheduler) | ellmos-ai | Lokale Cron-, Intervall- & Ausführungsengine für geplante Aufgaben |
| [clutch](https://github.com/ellmos-ai/clutch) | ellmos-ai | Adaptiver Multi-Modell-LLM-Router & Agenten-Ausführungssteuerung |
| [coma](https://github.com/ellmos-ai/coma) | ellmos-ai | Standalone Multi-Agenten-Orchestrierer & Koordinations-Engine |
| [gardener](https://github.com/ellmos-ai/gardener) | ellmos-ai | Lokale autonome Sitzungs- und Kontextgedächtnis-Engine |
| [prompt-evidence-collector](https://github.com/ellmos-ai/prompt-evidence-collector) | ellmos-ai | Revisionssichere LLM-Interaktionserfassung & kryptografischer Beweisspeicher |
| [lock-master](https://github.com/ellmos-ai/lock-master) | ellmos-ai | Multi-Agenten-Dateisperr- und Nebenläufigkeits-Kontrollprotokoll |
| [ticket-master](https://github.com/ellmos-ai/ticket-master) | ellmos-ai | Autonome Ticket-Routing- und Aufgaben-Dispatching-Triagekonsole |
| [ellmos-controlcenter-mcp](https://github.com/ellmos-ai/ellmos-controlcenter-mcp) | ellmos-ai | MCP-Laufzeitüberwachung, Skill-Routing & Werkzeugbündel-Erkennung |
| [ellmos-filecommander-mcp](https://github.com/ellmos-ai/ellmos-filecommander-mcp) | ellmos-ai | MCP-Dateiverwaltung, sichere Löschung & Archivierungs-Server |
| [ellmos-codecommander-mcp](https://github.com/ellmos-ai/ellmos-codecommander-mcp) | ellmos-ai | MCP-Codeanalyse, AST-Transformationen & Formatierungs-Server |
| [ellmos-clatcher-mcp](https://github.com/ellmos-ai/ellmos-clatcher-mcp) | ellmos-ai | MCP-Zwischenablage & Notizblock-Manager mit Dry-Run-Sicherheit |
| [n8n-manager-mcp](https://github.com/ellmos-ai/n8n-manager-mcp) | ellmos-ai | MCP-n8n-Workflow-Management, Ausführungsüberwachung & Node-Introspektion |
| [skills](https://github.com/ellmos-ai/skills) | ellmos-ai | Kanonische Multi-Agenten-Fähigkeitsbibliothek & Agenten-Katalog |
| [usb-podcast-studio](https://github.com/entertain-and-more/usb-podcast-studio) | entertain-and-more | Desktop-Audio-Workstation, Soundboard & Aufnahme-Suite (Klangpult) |
| [companion-for-agy](https://github.com/ellmos-ai/companion-for-agy) | ellmos-ai | Terminal-Begleiter & PTY-Wrapper für Google Antigravity |
| [safe-start-for-codex](https://github.com/dev-bricks/safe-start-for-codex) | dev-bricks | Sicherer Starter und Berechtigungsisolator für Codex CLI-Sitzungen |
| [automizer-for-claude-desktop](https://github.com/dev-bricks/automizer-for-claude-desktop) | dev-bricks | Aufgaben-Automationsmanager für Claude Desktop |
| [DevCenter](https://github.com/dev-bricks/DevCenter) | dev-bricks | Entwickler-Leitstand, Repository-Dashboard & Umgebungsmanager |
| [CodeBox](https://github.com/dev-bricks/CodeBox) | dev-bricks | Polyglotter Code-Snippet-Manager & Entwickler-Werkbank |
| [WikiStub-Seed](https://github.com/dev-bricks/WikiStub-Seed) | dev-bricks | Mehrsprachiges JSON-Wissensskelett mit 630 Stubs über 12 Domänen |
| [automation-master](https://github.com/ellmos-ai/automation-master) | ellmos-ai | Multi-Host-Automations- & Scheduled-Task-Register |
| [WinStorePackager](https://github.com/file-bricks/WinStorePackager) | file-bricks | Windows Store Packaging-, MSIX-Erstellungs- & Release-Tool |
| [policy-registry](https://github.com/ellmos-ai/policy-registry) | ellmos-ai | Autonomous compliance, audit and policy governance store |
| [open-bricks](https://github.com/open-bricks) | open-bricks | Dachkatalog für Open-Source-Bausteine, Werkzeuge und Bibliotheken |

---

## 13. Entwicklungsstatus & Roadmap

Die aktuellen Gatter und die nächsten prüfbaren Schritte stehen in [`ROADMAP.md`](ROADMAP.md).
Das Repository ist öffentlich auf GitHub und das Paket nicht auf PyPI veröffentlicht.
Sichtbarkeit, Tag, Release oder Registry-Upload benötigen eine gesonderte
Eigentümerentscheidung; siehe [`RELEASE_GATE.md`](RELEASE_GATE.md).

---

## 14. Provenienz & Historien-Grenze

Das Modul erhält den generischen, MIT-lizenzierten Kern eines früheren internen
Sprachdienstes: Datei-STT, TTS-Dateiexport und Wake-Word-Anbindung. Es wurde als
unabhängiges, nutzungsneutrales Paket neu aufgebaut – ohne Bindungen an frühere
Datenbanken oder Bridges.

---

## 15. Sicherheitsrichtlinie & Meldewege

Sicherheits- und Datenschutz-Invarianten werden strikt eingehalten. Details zu koordinierter Offenlegung, unterstützten Versionen und unserem 48-Stunden-Reaktions-SLA finden sich in [`SECURITY.md`](SECURITY.md).

---

## 16. Lizenz, Urheberrecht & Englische Dokumentation

Code und Dokumentation dieses Repositories stehen unter der MIT-Lizenz; siehe
[LICENSE](LICENSE). Optionale Engines, Systemwerkzeuge sowie Stimmen und
Modelldateien behalten ihre eigenen Lizenzen; siehe
[THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md). Verantwortungs- und
Einsatzgrenzen stehen in [SECURITY.md](SECURITY.md) und
[docs/ai-act-note.md](docs/ai-act-note.md). Für Beiträge gelten
[CONTRIBUTING.md](CONTRIBUTING.md) und [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

Die englische Ausgabe dieser Dokumentation finden Sie unter **[README.md](README.md)**.
