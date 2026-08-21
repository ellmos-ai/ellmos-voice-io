# Third-party licenses

`ellmos-voice-io` itself is MIT licensed. The base wheel contains none of the
optional engines below; users install selected extras separately. Each package,
its transitive dependencies, system libraries, and every voice/model file keep
their own license and terms.

| Optional component | Declared use | Upstream license at review | Source |
|---|---|---|---|
| `openai-whisper` | Local file STT | MIT | <https://github.com/openai/whisper> |
| `vosk` | Offline file STT | Apache-2.0 | <https://github.com/alphacep/vosk-api> |
| `pyttsx3` | System-voice TTS | MPL-2.0 | <https://github.com/nateshmbhat/pyttsx3> |
| `piper-tts` | ONNX TTS | **GPL-3.0-or-later** | <https://github.com/OHF-Voice/piper1-gpl> |
| `openwakeword` | Local wake-word evaluation | Apache-2.0 | <https://github.com/dscripka/openWakeWord> |
| `PyAudio` | Microphone stream adapter | MIT according to the package registry | <https://pypi.org/project/PyAudio/> |
| `NumPy` | Audio-array conversion | BSD-3-Clause plus bundled-component notices | <https://github.com/numpy/numpy> |
| FFmpeg executable | Optional MP3/OGG conversion | Build-dependent LGPL/GPL terms | <https://ffmpeg.org/legal.html> |

Review date: 2026-08-21. This is an inventory, not a relicensing of those
components. In particular:

- The `all` extra installs `piper-tts`; distributing a combined environment or
  product requires review of its GPL obligations.
- Whisper, Vosk, Piper, openWakeWord, and operating-system voices may use
  separately licensed model or voice files. This repository does not bundle
  or authorize redistribution of any such file.
- FFmpeg is invoked only when a caller requests MP3 or OGG output. The caller's
  installed build determines the applicable license and codecs.
