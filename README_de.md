# ellmos-voice-io

Lokale Speech-to-Text-, Text-to-Speech- und Wake-Word-Hilfen für LLM-Systeme.

`ellmos-voice-io` ist ein kleines, LLM-neutrales Laufzeitmodul. Es startet keinen
Server, speichert keine Aufnahmen, liefert keine Stimmmodelle aus und wählt keinen
Cloud-Provider. Aufrufer wählen optionale lokale Engines ausdrücklich und verantworten
Mikrofonberechtigungen, Modelldownloads, Aufbewahrung und jede Netzwerkintegration.

## Umfang

- Dateibasierte STT über optionales Whisper oder Vosk.
- TTS auf Lautsprecher oder in Dateien über optionales pyttsx3 oder Piper.
- Lokale Mikrofon-Wake-Word-Erkennung über optionales openWakeWord.
- Stabile Python-API und eine rein lesende `status`-CLI für Skills, MCP-Adapter und Apps.

Das Modul ersetzt bewusst keine Audio-Workstations wie KlangpultLight oder
USBPodcastStudio. Deren Aufnahme-, Schnitt-, Streaming- und Transkript-Workflows bleiben
anwendungsspezifische Konsumenten dieser engeren Fähigkeit.

## Installation

```bash
pip install ellmos-voice-io
pip install "ellmos-voice-io[stt-vosk,tts-pyttsx3]"
ellmos-voice-io status
```

Aktualisierung: `pip install --upgrade ellmos-voice-io`. Optionale Engines werden nicht
standardmäßig installiert. Whisper kann beim ersten Einsatz ein Modell herunterladen;
Vosk und Piper benötigen einen ausdrücklich angegebenen lokalen Modellpfad.

## Datenschutz und Grenzen

- Audio, Transkripte und Ausgabedateien bleiben am vom Aufrufer bestimmten Ort.
- Kein Datenbankzugriff, keine Telemetrie, kein Konto, kein Hintergrunddienst, kein Upload.
- Mikrofonzugriff erfolgt erst mit `WakeWordListener.listen()`.
- Das Ergebnis von `status` ist kein Berechtigungs- oder Deployment-Nachweis.

## Herkunft

Das Modul rettet den generischen, MIT-lizenzierten Kern des früheren BACH Voice Service:
Datei-STT, TTS-Dateiexport und Wake-Word-Anbindung. Es wurde als unabhängiges,
nutzungsneutrales Paket neu aufgebaut – ohne BACH-Datenbank oder Bridge-Bindungen.
