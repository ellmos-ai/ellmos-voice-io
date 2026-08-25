<p align="center">
  <img src="docs/assets/banner.png" alt="ellmos-voice-io: local microphone, speech processing, and speaker flow" width="900">
</p>

# ellmos-voice-io

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-0.2.0-blue.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-40%20passed-brightgreen?logo=pytest&logoColor=white)](tests/)
[![Privacy: Local-First](https://img.shields.io/badge/Privacy-Local--First%20%7C%20No--Telemetry-blue)](README.md#privacy-and-boundaries)
[![llms.txt](https://img.shields.io/badge/llms.txt-available-0055ff?logo=markdown)](llms.txt)
[![Org](https://img.shields.io/badge/Org-ellmos--ai-8A2BE2)](https://github.com/ellmos-ai)
[![Ecosystem](https://img.shields.io/badge/Ecosystem-open--bricks-blue)](https://github.com/open-bricks)

**[English](README.md)** | **[Deutsch](README_de.md)**

> [!TIP]
> **Machine-Readable Documentation:** An [`llms.txt`](llms.txt) index is provided for AI agents, LLMs, and automated RAG pipelines.

Local-first speech input, speech output, and wake-word helpers for LLM systems.

`ellmos-voice-io` is a small, LLM-neutral runtime module. It does not run a server, store recordings, ship voice models, or choose a cloud provider. A caller explicitly selects optional local engines and owns all microphone permissions, model downloads, retention, and any networked integration.

---

## Architecture Overview

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

## Scope & Capabilities

- **File-based STT**: Speech-to-Text through optional Whisper or Vosk.
- **File & Speaker TTS**: Text-to-Speech to speakers or files through optional pyttsx3 or Piper.
- **Local Wake-Word**: Real-time microphone wake-word detection through optional openWakeWord.
- **Stable Python API & Read-Only CLI**: Inspection via `status` CLI for Skills, MCP adapters, and desktop apps.

| Capability | Supported Engines | Input / Output | Key Feature |
|---|---|---|---|
| **Speech-to-Text** | `vosk`, `whisper` | `.wav` file $\to$ string | Fully offline with local model |
| **Text-to-Speech** | `pyttsx3`, `piper` | string $\to$ `.wav` / `.mp3` / `.ogg` or speaker | System voices or neural ONNX synthesis |
| **Wake-Word** | `openwakeword` | Microphone stream $\to$ callback | Synchronous, caller-owned stop event |

It intentionally does not replace audio workstations such as KlangpultLight or USBPodcastStudio. Their recording, editing, streaming, and transcript workflows remain application-specific consumers of this narrower capability.

---

## Installation

The package is not published to PyPI yet. Until an owner-approved release exists,
install it only from a trusted local checkout:

```bash
# Minimal base package (no optional heavy dependencies)
python -m pip install .

# Install with specific optional extras
python -m pip install ".[stt-vosk,tts-pyttsx3]"

# Development and verification toolchain
python -m pip install -e ".[dev]"
```

The `all` extra also installs `piper-tts`, whose current distribution is
GPL-3.0-or-later. Review [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md)
and the licenses of any selected voice/model files before redistribution.

Inspect engine status safely without starting hardware:
```bash
ellmos-voice-io status
```

Output:
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

## Python API Examples

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

## Privacy and Boundaries

- **Audio, transcripts, and generated files stay where the caller puts them.**
- **No telemetry, database, account requirement, background service, or implicit upload.**
- **Microphone access occurs only during active `WakeWordListener.listen()`.**
- **No implicit Whisper download**: provide a local model file or opt in with
  `allow_model_download=True`; the caller then owns network and model-license policy.
- **Read-only CLI**: `status` never attempts permissions or model downloads.

### Wake-Word Lifecycle Contract

`WakeWordListener.listen(on_wake, stop_event)` is synchronous and caller-owned:
- A pre-set stop event returns immediately without opening audio hardware.
- Every audio chunk with a prediction at or above the threshold invokes the callback once. Debouncing remains caller policy.
- The stop event is checked before every read cycle. Model, stream, and read exceptions propagate safely after audio stream termination and cleanup.

---

## Development Status & Roadmap

The current development gates, task plans, and next verifiable milestones are documented in [`ROADMAP.md`](ROADMAP.md).
The repository is still private and the package is not on PyPI. A visibility,
tag, release, or registry upload requires a separate owner decision; see
[`RELEASE_GATE.md`](RELEASE_GATE.md).

---

## Provenance

This module preserves the generic, MIT-licensed core of an earlier internal
voice service: file STT, TTS file export, and wake-word integration. It is
rewritten as an independent, user-neutral package with explicit dependencies
and no legacy database or bridge bindings.

## Ecosystem & Sibling Tools

Part of the [ellmos-ai](https://github.com/ellmos-ai) multi-agent infrastructure and the overarching [open-bricks](https://github.com/open-bricks) open-source software ecosystem:

| Tool | Organization | Description |
|------|--------------|-------------|
| [ellmos-core](https://github.com/ellmos-ai/ellmos-core) | ellmos-ai | Modular AI runtime, task dispatching & agent state substrate |
| [ellmos-scheduler](https://github.com/ellmos-ai/ellmos-scheduler) | ellmos-ai | Local cron, interval & scheduled task execution engine |
| [clutch](https://github.com/ellmos-ai/clutch) | ellmos-ai | Adaptive multi-model LLM router & agent execution gear |
| [coma](https://github.com/ellmos-ai/coma) | ellmos-ai | Single-binary multi-agent orchestrator & execution coordinator |
| [gardener](https://github.com/ellmos-ai/gardener) | ellmos-ai | Local-first autonomous session and context memory engine |
| [prompt-evidence-collector](https://github.com/ellmos-ai/prompt-evidence-collector) | ellmos-ai | Audit-ready LLM interaction capture & cryptographic evidence store |
| [lock-master](https://github.com/ellmos-ai/lock-master) | ellmos-ai | Multi-agent file locking and concurrency control protocol |
| [ticket-master](https://github.com/ellmos-ai/ticket-master) | ellmos-ai | Autonomous ticket routing and task dispatching triage console |
| [ellmos-controlcenter-mcp](https://github.com/ellmos-ai/ellmos-controlcenter-mcp) | ellmos-ai | MCP runtime supervision, skill routing & tool bundle discovery |
| [ellmos-filecommander-mcp](https://github.com/ellmos-ai/ellmos-filecommander-mcp) | ellmos-ai | MCP file management, safe delete & archive operations server |
| [ellmos-codecommander-mcp](https://github.com/ellmos-ai/ellmos-codecommander-mcp) | ellmos-ai | MCP code analysis, AST transformations & format server |
| [ellmos-clatcher-mcp](https://github.com/ellmos-ai/ellmos-clatcher-mcp) | ellmos-ai | MCP clipboard & scratchpad manager with dry-run safety |
| [n8n-manager-mcp](https://github.com/ellmos-ai/n8n-manager-mcp) | ellmos-ai | MCP n8n workflow management, execution monitoring & node introspection |
| [skills](https://github.com/ellmos-ai/skills) | ellmos-ai | Multi-agent canonical capability library & agent catalog |
| [usb-podcast-studio](https://github.com/entertain-and-more/usb-podcast-studio) | entertain-and-more | Desktop audio workstation, soundboard & recording suite (Klangpult) |
| [companion-for-agy](https://github.com/ellmos-ai/companion-for-agy) | ellmos-ai | Terminal companion & PTY wrapper for Google Antigravity |
| [safe-start-for-codex](https://github.com/dev-bricks/safe-start-for-codex) | dev-bricks | Safe starter and permission isolator for Codex CLI sessions |
| [automizer-for-claude-desktop](https://github.com/dev-bricks/automizer-for-claude-desktop) | dev-bricks | Scheduled task automation manager for Claude Desktop |
| [DevCenter](https://github.com/dev-bricks/DevCenter) | dev-bricks | Developer control plane, repository dashboard & environment manager |
| [CodeBox](https://github.com/dev-bricks/CodeBox) | dev-bricks | Polyglot code snippet manager & developer workbench |
| [open-bricks](https://github.com/open-bricks) | open-bricks | Umbrella catalog for open-source bricks, tools, and libraries |

---

## License

The repository's code and documentation are MIT licensed; see [LICENSE](LICENSE).
Optional engines, system tools, and voice/model files retain their own licenses;
see [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md). Responsible-use and
deployment boundaries are documented in [SECURITY.md](SECURITY.md) and
[docs/ai-act-note.md](docs/ai-act-note.md). Contributions follow
[CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
