"""Composable service facade for LLM tools, CLIs, or MCP adapters."""

from __future__ import annotations

from dataclasses import asdict, dataclass

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
