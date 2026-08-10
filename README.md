# ellmos-voice-io

Local-first speech input, speech output, and wake-word helpers for LLM systems.

`ellmos-voice-io` is a small, LLM-neutral runtime module. It does not run a server,
store recordings, ship voice models, or choose a cloud provider. A caller explicitly
selects optional local engines and owns all microphone permissions, model downloads,
retention, and any networked integration.

## Scope

- File-based STT through optional Whisper or Vosk.
- TTS to speakers or files through optional pyttsx3 or Piper.
- Local microphone wake-word detection through optional openWakeWord.
- A stable Python API and read-only `status` CLI for Skills, MCP adapters, and apps.

It intentionally does not replace audio workstations such as KlangpultLight or
USBPodcastStudio. Their recording, editing, streaming, and transcript workflows remain
application-specific consumers of this narrower capability.

## Development status

The current development gates and next verifiable work are tracked in
[`ROADMAP.md`](ROADMAP.md). The manifest is still `development`/`private`; no
package publish or external release is implied by the installation examples.

## Install

```bash
pip install ellmos-voice-io
pip install "ellmos-voice-io[stt-vosk,tts-pyttsx3]"
ellmos-voice-io status
```

Use `pip install --upgrade ellmos-voice-io` for updates. Optional engines are not
installed by default. Whisper may download a model on first use; Vosk and Piper require
an explicit local model path.

## Python API

```python
from ellmos_voice_io import SpeechToText, TextToSpeech, VoiceIO

print(VoiceIO().status().as_dict())
text = SpeechToText(engine="vosk", model_path="/models/vosk-de").transcribe_file("note.wav")
TextToSpeech(engine="pyttsx3").speak_to_file(text, "reply.wav")
```

## Privacy and boundaries

- Audio, transcripts, and generated files stay where the caller puts them.
- The package has no database, telemetry, account, background service, or implicit upload.
- Microphone access happens only when the caller invokes `WakeWordListener.listen()`.
- Never treat the `status` result as a permission or deployment check.

### Wake-word lifecycle

`WakeWordListener.listen(on_wake, stop_event)` is synchronous and caller-owned:

- a pre-set stop event returns without opening the microphone;
- every audio chunk with a prediction at or above the threshold invokes the callback once,
  so repeated qualifying chunks produce repeated callbacks and debouncing remains a caller
  policy;
- a stop event is checked before every read; callback, model, stream, and read exceptions
  propagate after the stream is stopped/closed and the PyAudio instance is terminated.

## Provenance

This module rescues the generic, MIT-licensed core of BACH's former Voice Service:
file STT, TTS file export, and wake-word integration. It is rewritten as an independent,
user-neutral package with explicit dependencies and no BACH database or bridge bindings.
