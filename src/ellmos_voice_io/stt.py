"""Optional speech-to-text engines with no network use unless the engine needs it."""

from __future__ import annotations

import json
import os
import wave
from importlib.util import find_spec
from pathlib import Path


class SpeechToText:
    """Transcribe an existing audio file with Whisper or Vosk.

    ``whisper`` requires either an explicit local ``model_path`` or the explicit
    ``allow_model_download=True`` opt-in for a named model. ``vosk`` stays local
    and requires an explicit ``model_path`` or ``VOSK_MODEL`` environment variable.
    """

    def __init__(
        self,
        engine: str = "auto",
        model_size: str = "base",
        model_path: str | Path | None = None,
        *,
        allow_model_download: bool = False,
    ):
        if engine not in {"auto", "whisper", "vosk"}:
            raise ValueError("engine must be auto, whisper, or vosk")
        self.engine = engine
        self.model_size = model_size
        self.model_path = model_path
        self.allow_model_download = allow_model_download
        self._whisper_model = None
        self._vosk_model = None

    def available(self) -> tuple[bool, str]:
        if self.engine in {"auto", "whisper"} and find_spec("whisper") is not None:
            return True, "whisper"
        if self.engine in {"auto", "vosk"} and find_spec("vosk") is not None:
            return True, "vosk"
        return False, "Install an optional STT extra: stt-whisper or stt-vosk."

    def transcribe_file(self, audio_path: str | Path, language: str | None = "de") -> str:
        path = Path(audio_path).expanduser()
        if not path.is_file():
            raise FileNotFoundError(path)
        available, engine = self.available()
        if not available:
            raise RuntimeError(engine)
        if engine == "whisper":
            return self._transcribe_whisper(path, language)
        return self._transcribe_vosk(path)

    def _transcribe_whisper(self, path: Path, language: str | None) -> str:
        import whisper

        if self._whisper_model is None:
            if self.model_path is not None:
                local_model = Path(self.model_path).expanduser()
                if not local_model.is_file():
                    raise FileNotFoundError(local_model)
                model_ref = str(local_model)
            elif self.allow_model_download:
                model_ref = self.model_size
            else:
                raise RuntimeError(
                    "Whisper named models may access the network when missing. "
                    "Pass a local model_path or set allow_model_download=True explicitly."
                )
            self._whisper_model = whisper.load_model(model_ref)
        result = self._whisper_model.transcribe(str(path), language=language)
        return str(result.get("text", "")).strip()

    def _transcribe_vosk(self, path: Path) -> str:
        import vosk

        model_path = self.model_path or os.environ.get("VOSK_MODEL")
        if not model_path or not Path(model_path).is_dir():
            raise RuntimeError("Vosk needs a valid model_path or VOSK_MODEL directory.")
        if self._vosk_model is None:
            vosk.SetLogLevel(-1)
            self._vosk_model = vosk.Model(model_path)
        with wave.open(str(path), "rb") as audio:
            recognizer = vosk.KaldiRecognizer(self._vosk_model, audio.getframerate())
            parts: list[str] = []
            while data := audio.readframes(4_000):
                if recognizer.AcceptWaveform(data):
                    parts.append(json.loads(recognizer.Result()).get("text", ""))
            parts.append(json.loads(recognizer.FinalResult()).get("text", ""))
        return " ".join(part for part in parts if part).strip()
