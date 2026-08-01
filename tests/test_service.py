from pathlib import Path
import sys

import pytest

from ellmos_voice_io.service import VoiceIO
from ellmos_voice_io.stt import SpeechToText
from ellmos_voice_io.tts import TextToSpeech
from ellmos_voice_io.wakeword import WakeWordListener
from ellmos_voice_io.cli import main


def test_status_is_serializable():
    status = VoiceIO().status().as_dict()
    assert set(status) == {"stt_available", "stt_engine", "tts_available", "tts_engine", "wakeword_available", "wakeword_engine"}


def test_invalid_engine_is_rejected():
    with pytest.raises(ValueError):
        SpeechToText(engine="remote")
    with pytest.raises(ValueError):
        TextToSpeech(engine="browser")


def test_missing_audio_file_fails_before_engine_lookup(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        SpeechToText().transcribe_file(tmp_path / "missing.wav")


def test_tts_requires_supported_extension(tmp_path: Path):
    with pytest.raises(ValueError):
        TextToSpeech().speak_to_file("hello", tmp_path / "speech.txt")


def test_wakeword_threshold_is_bounded():
    with pytest.raises(ValueError):
        WakeWordListener(0)
    with pytest.raises(ValueError):
        WakeWordListener(1.1)


def test_status_cli_is_read_only(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["ellmos-voice-io", "status"])
    assert main() == 0
    assert "stt_available" in capsys.readouterr().out
