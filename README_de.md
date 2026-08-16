# ellmos-voice-io

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-20%20bestanden-brightgreen?logo=pytest&logoColor=white)](tests/)
[![Privacy: Local-First](https://img.shields.io/badge/Datenschutz-Local--First%20%7C%20Keine--Telemetrie-blue)](README_de.md#datenschutz-und-grenzen)
[![llms.txt](https://img.shields.io/badge/llms.txt-verf%C3%BCgbar-0055ff?logo=markdown)](llms.txt)
[![Org](https://img.shields.io/badge/Org-ellmos--ai-8A2BE2)](https://github.com/ellmos-ai)
[![Ecosystem](https://img.shields.io/badge/Ecosystem-open--bricks-blue)](https://github.com/open-bricks)

**[English](README.md)** | **[Deutsch](README_de.md)**

> [!TIP]
> **Maschinenlesbare Dokumentation:** Ein [`llms.txt`](llms.txt)-Index steht für KI-Agenten, LLMs und automatisierte RAG-Pipelines bereit.

Lokale Speech-to-Text-, Text-to-Speech- und Wake-Word-Hilfen für LLM-Systeme.

`ellmos-voice-io` ist ein kleines, LLM-neutrales Laufzeitmodul. Es startet keinen Server, speichert keine Aufnahmen, liefert keine Stimmmodelle aus und wählt keinen Cloud-Provider. Aufrufer wählen optionale lokale Engines ausdrücklich und verantworten Mikrofonberechtigungen, Modelldownloads, Aufbewahrung und jede Netzwerkintegration.

---

## Architektur-Übersicht

```mermaid
graph TD
    UserApp["Aufrufer / LLM-Anwendung / MCP-Adapter"]
    
    subgraph FacadeLayer ["ellmos-voice-io Laufzeit"]
        VoiceIO["VoiceIO (Einheitliche Fassade)"]
        CLI["CLI (ellmos-voice-io status)"]
        STT["SpeechToText"]
        TTS["TextToSpeech"]
        WakeWord["WakeWordListener"]
    end
    
    subgraph OptionalEngines ["Optionale Lazy Engines"]
        Vosk["Vosk (Lokales Offline STT)"]
        Whisper["Whisper (Neuronales STT)"]
        Pyttsx3["pyttsx3 (System-TTS)"]
        Piper["Piper (ONNX Neuronales TTS)"]
        OpenWakeWord["openWakeWord (Lokales Mikrofon)"]
    end
    
    subgraph PrivacyBoundary ["Datenschutz- & Hardware-Grenze"]
        Mic["Mikrofon (Explizit autorisiert)"]
        AudioFiles["Lokale WAV / MP3 / OGG Dateien"]
        ZeroNet["Keine Telemetrie / Kein Cloud-Upload"]
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

## Umfang & Fähigkeiten

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

## Installation

```bash
# Minimales Basispaket (ohne schwere optionale Abhängigkeiten)
pip install ellmos-voice-io

# Installation mit spezifischen optionalen Extras
pip install "ellmos-voice-io[stt-vosk,tts-pyttsx3]"

# Oder Installation aller verfügbaren lokalen Engines
pip install "ellmos-voice-io[all]"
```

Engine-Verfügbarkeit sicher prüfen ohne Hardware-Initialisierung:
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

## Python API Beispiele

### Speech-to-Text (STT)

```python
from ellmos_voice_io import SpeechToText

# Vosk mit lokalem Modellpfad
stt = SpeechToText(engine="vosk", model_path="/pfad/zu/vosk-model-de")
transkript = stt.transcribe_file("input_voice.wav")
print(f"Transkribiert: {transkript}")

# Whisper
stt_whisper = SpeechToText(engine="whisper", model_size="base")
transkript_whisper = stt_whisper.transcribe_file("aufnahme.wav", language="de")
```

### Text-to-Speech (TTS)

```python
from ellmos_voice_io import TextToSpeech

tts = TextToSpeech(engine="pyttsx3", rate=160)

# Direkte Sprachausgabe auf Systemlautsprecher
tts.speak("Verarbeitung abgeschlossen.")

# Synthese in eine Audiodatei (.wav, .mp3, .ogg) exportieren
tts.speak_to_file("Benachrichtigungston erzeugt.", "output/meldung.wav")
```

### Wake-Word Listener

```python
import threading
from ellmos_voice_io import WakeWordListener

def on_wake():
    print("Wake-Word erkannt! Assistent wird aktiviert...")

stop_event = threading.Event()
listener = WakeWordListener(threshold=0.6)

# Blockiert synchron bis stop_event gesetzt wird; bereinigt Audio-Streams automatisch
listener.listen(on_wake=on_wake, stop_event=stop_event)
```

---

## Datenschutz und Grenzen

- **Audio, Transkripte und Ausgabedateien bleiben am vom Aufrufer bestimmten Ort.**
- **Kein Datenbankzugriff, keine Telemetrie, kein Konto, kein Hintergrunddienst, kein impliziter Upload.**
- **Mikrofonzugriff erfolgt ausschließlich während aktivem `WakeWordListener.listen()`.**
- **Rein lesende CLI**: `status` fordert keine Berechtigungen an und lädt keine Modelle herunter.

### Wake-Word-Lebenszyklus

`WakeWordListener.listen(on_wake, stop_event)` ist synchron und aufrufer-kontrolliert:
- Ein vorab gesetztes `stop_event` kehrt sofort zurück, ohne Audiogeräte zu öffnen.
- Jeder Audio-Chunk mit einer Vorhersage $\ge$ Schwellenwert löst den Callback genau einmal aus. Entprellung verbleibt beim Aufrufer.
- Das `stop_event` wird vor jedem Leseschritt geprüft. Modell-, Stream- und Lese-Ausnahmen werden nach geordnetem Beenden des Audiostreams sicher weitergereicht.

---

## Entwicklungsstatus & Roadmap

Die aktuellen Gatter und die nächsten prüfbaren Schritte stehen in [`ROADMAP.md`](ROADMAP.md).

---

## Herkunft

Das Modul rettet den generischen, MIT-lizenzierten Kern des früheren BACH Voice Service: Datei-STT, TTS-Dateiexport und Wake-Word-Anbindung. Es wurde als unabhängiges, nutzungsneutrales Paket neu aufgebaut – ohne BACH-Datenbank oder Bridge-Bindungen.

## Lizenz

MIT Lizenz. Siehe [LICENSE](LICENSE) für Details.
