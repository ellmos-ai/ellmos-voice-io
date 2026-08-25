"""Optional local text-to-speech engines."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import wave
from importlib.util import find_spec
from pathlib import Path


class TextToSpeech:
    """Speak text or write it to an audio file using an explicitly selected engine."""

    def __init__(self, engine: str = "auto", rate: int = 170, voice_name: str = "auto", piper_model: str | None = None):
        if engine not in {"auto", "pyttsx3", "piper"}:
            raise ValueError("engine must be auto, pyttsx3, or piper")
        self.engine, self.rate, self.voice_name, self.piper_model = engine, rate, voice_name, piper_model
        self._pyttsx3_engine = None
        self._piper_voice = None

    def available(self) -> tuple[bool, str]:
        if self.engine in {"auto", "pyttsx3"} and find_spec("pyttsx3") is not None:
            return True, "pyttsx3"
        if self.engine in {"auto", "piper"} and find_spec("piper") is not None:
            return True, "piper"
        return False, "Install an optional TTS extra: tts-pyttsx3 or tts-piper."

    def speak(self, text: str) -> None:
        if not text.strip():
            raise ValueError("text must not be blank")
        available, engine = self.available()
        if not available:
            raise RuntimeError(engine)
        if engine != "pyttsx3":
            raise RuntimeError("Piper only supports file output; use speak_to_file.")
        speaker = self._ensure_pyttsx3()
        self._apply_voice(speaker)
        speaker.say(text)
        speaker.runAndWait()

    def speak_to_file(self, text: str, output_path: str | Path) -> Path:
        if not text.strip():
            raise ValueError("text must not be blank")
        output = Path(output_path).expanduser()
        if output.suffix.lower() not in {".wav", ".mp3", ".ogg"}:
            raise ValueError("output_path must end in .wav, .mp3, or .ogg")
        output.parent.mkdir(parents=True, exist_ok=True)
        available, engine = self.available()
        if not available:
            raise RuntimeError(engine)
        if engine == "piper":
            return self._piper_to_file(text, output)
        return self._pyttsx3_to_file(text, output)

    def _ensure_pyttsx3(self):
        if self._pyttsx3_engine is None:
            import pyttsx3

            self._pyttsx3_engine = pyttsx3.init()
            self._pyttsx3_engine.setProperty("rate", self.rate)
        return self._pyttsx3_engine

    def _apply_voice(self, speaker) -> None:
        if self.voice_name == "auto":
            return
        for voice in speaker.getProperty("voices"):
            if self.voice_name.lower() in voice.name.lower():
                speaker.setProperty("voice", voice.id)
                return
        raise RuntimeError(f"Requested voice not found: {self.voice_name}")

    def _pyttsx3_to_file(self, text: str, output: Path) -> Path:
        speaker = self._ensure_pyttsx3()
        self._apply_voice(speaker)
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "speech.wav"
            speaker.save_to_file(text, str(source))
            speaker.runAndWait()
            if not source.exists():
                raise RuntimeError("pyttsx3 did not create an audio file")
            return self._convert_or_copy(source, output)

    def _piper_to_file(self, text: str, output: Path) -> Path:
        if not self.piper_model:
            raise RuntimeError("Piper needs an explicit piper_model path.")
        model = Path(self.piper_model).expanduser()
        if not model.is_file():
            raise FileNotFoundError(model)
        from piper import PiperVoice

        if self._piper_voice is None:
            self._piper_voice = PiperVoice.load(str(model))
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "speech.wav"
            with wave.open(str(source), "wb") as wav_file:
                self._piper_voice.synthesize(text, wav_file)
            return self._convert_or_copy(source, output)

    @staticmethod
    def _convert_or_copy(source: Path, output: Path) -> Path:
        if output.suffix.lower() == ".wav":
            shutil.copyfile(source, output)
            return output
        try:
            subprocess.run(["ffmpeg", "-y", "-i", str(source), str(output)], check=True, capture_output=True)
        except FileNotFoundError as error:
            raise RuntimeError("ffmpeg is required for .mp3 and .ogg output.") from error
        return output
