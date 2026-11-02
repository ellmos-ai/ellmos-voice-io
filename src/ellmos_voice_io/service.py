"""Composable service facade for LLM tools, CLIs, or MCP adapters."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import tempfile

from .stt import SpeechToText
from .tts import TextToSpeech
from .wakeword import WakeWordListener


@dataclass(frozen=True)
class VoiceStatus:
    stt_available: bool
    stt_engine: str
    tts_available: bool
    tts_engine: str
    wakeword_available: bool
    wakeword_engine: str

    def as_dict(self) -> dict[str, bool | str]:
        return asdict(self)


class VoiceIO:
    """Container that keeps optional engines explicit and independently replaceable."""

    def __init__(self, stt: SpeechToText | None = None, tts: TextToSpeech | None = None, wakeword: WakeWordListener | None = None):
        self.stt = stt or SpeechToText()
        self.tts = tts or TextToSpeech()
        self.wakeword = wakeword or WakeWordListener()

    def status(self) -> VoiceStatus:
        stt_ok, stt_engine = self.stt.available()
        tts_ok, tts_engine = self.tts.available()
        wake_ok, wake_engine = self.wakeword.available()
        return VoiceStatus(stt_ok, stt_engine, tts_ok, tts_engine, wake_ok, wake_engine)

    def transcribe_bytes(self, audio_bytes: bytes, *, suffix: str = ".wav", language: str | None = "de") -> str:
        """Transcribe raw audio bytes via a short-lived temporary file."""
        if not audio_bytes:
            raise ValueError("audio_bytes must not be empty")
        ext = suffix if suffix.startswith(".") else f".{suffix}"
        with tempfile.TemporaryDirectory(prefix="ellmos-voice-stt-") as tmp_dir:
            audio_path = Path(tmp_dir) / f"input{ext}"
            audio_path.write_bytes(audio_bytes)
            return self.stt.transcribe_file(audio_path, language=language)

    def synthesize_bytes(self, text: str, *, suffix: str = ".wav") -> bytes:
        """Synthesize text to audio bytes via a short-lived temporary file."""
        if not text.strip():
            raise ValueError("text must not be blank")
        ext = suffix if suffix.startswith(".") else f".{suffix}"
        with tempfile.TemporaryDirectory(prefix="ellmos-voice-tts-") as tmp_dir:
            out_path = Path(tmp_dir) / f"output{ext}"
            self.tts.speak_to_file(text, out_path)
            return out_path.read_bytes()
