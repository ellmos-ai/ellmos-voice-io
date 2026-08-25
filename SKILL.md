---
name: ellmos-voice-io
version: 0.2.0
type: service
author: ELLMOS AI
created: 2026-08-01
updated: 2026-08-21
anthropic_compatible: true
dependencies:
  tools: []
  services: []
  protocols: []
description: >
  Local-first STT, TTS, and wake-word primitives for LLM-connected applications.
---

# ellmos-voice-io

Use this module when an LLM system needs to transcribe an explicit audio file, create an
explicit audio response, or listen locally for a wake word. Begin with
`ellmos-voice-io status`; then select an optional engine deliberately.

- STT: prefer Vosk with a caller-provided local model path for offline use. Whisper
  requires an explicit local model file or `allow_model_download=True`; named models
  never download implicitly.
- TTS: use pyttsx3 for installed system voices or Piper with an explicit model file.
- Wake word: request and verify microphone permission at the application boundary.
- Do not upload audio, retain transcripts, or start background listening implicitly.

This is a runtime module, not an audio editor, recorder, meeting assistant, or cloud voice
provider. Applications own their UI, storage, consent, and transport policy.
