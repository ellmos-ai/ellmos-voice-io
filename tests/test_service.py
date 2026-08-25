import json
import builtins
from pathlib import Path
import sys
import threading
import types
import wave

import pytest

import ellmos_voice_io.stt as stt_module
import ellmos_voice_io.tts as tts_module
import ellmos_voice_io.wakeword as wakeword_module
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


def test_optional_engines_stay_lazy_during_construction(monkeypatch):
    optional_modules = {"whisper", "vosk", "pyttsx3", "piper", "numpy", "pyaudio", "openwakeword"}
    original_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name.split(".", 1)[0] in optional_modules:
            raise AssertionError(f"optional module imported eagerly: {name}")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", guarded_import)
    SpeechToText()
    TextToSpeech()
    WakeWordListener()


def test_missing_audio_file_fails_before_engine_lookup(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        SpeechToText().transcribe_file(tmp_path / "missing.wav")


def test_stt_vosk_contract_uses_fixture_audio_and_explicit_model(monkeypatch, tmp_path: Path):
    audio_path = tmp_path / "note.wav"
    with wave.open(str(audio_path), "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(16_000)
        audio.writeframes(b"\x00\x00" * 128)
    model_path = tmp_path / "vosk-model"
    model_path.mkdir()
    calls: dict[str, object] = {}

    class FakeModel:
        def __init__(self, path: str):
            calls["model_path"] = path

    class FakeRecognizer:
        def __init__(self, model, rate: int):
            calls["sample_rate"] = rate

        def AcceptWaveform(self, data: bytes) -> bool:
            calls["frames"] = len(data)
            return True

        def Result(self) -> str:
            return json.dumps({"text": "hello"})

        def FinalResult(self) -> str:
            return json.dumps({"text": "world"})

    fake_vosk = types.SimpleNamespace(
        SetLogLevel=lambda level: calls.setdefault("log_level", level),
        Model=FakeModel,
        KaldiRecognizer=FakeRecognizer,
    )
    monkeypatch.setattr(stt_module, "find_spec", lambda name: object() if name == "vosk" else None)
    monkeypatch.setitem(sys.modules, "vosk", fake_vosk)

    result = SpeechToText(engine="vosk", model_path=model_path).transcribe_file(audio_path)

    assert result == "hello world"
    assert calls["model_path"] == model_path
    assert calls["sample_rate"] == 16_000
    assert calls["log_level"] == -1


def _install_whisper_double(monkeypatch, calls: dict[str, object]) -> None:
    class FakeWhisperModel:
        def transcribe(self, path: str, language: str | None = None):
            calls["transcribe"] = (path, language)
            return {"text": "local transcript"}

    def load_model(model_ref: str):
        calls["model_ref"] = model_ref
        return FakeWhisperModel()

    monkeypatch.setattr(SpeechToText, "available", lambda self: (True, "whisper"))
    monkeypatch.setitem(sys.modules, "whisper", types.SimpleNamespace(load_model=load_model))


def test_whisper_named_model_requires_explicit_download_opt_in(monkeypatch, tmp_path: Path):
    audio_path = tmp_path / "note.wav"
    audio_path.write_bytes(b"fixture")
    calls: dict[str, object] = {}
    _install_whisper_double(monkeypatch, calls)

    with pytest.raises(RuntimeError, match="allow_model_download"):
        SpeechToText(engine="whisper", model_size="base").transcribe_file(audio_path)

    assert "model_ref" not in calls


def test_whisper_named_model_allows_explicit_download_opt_in(monkeypatch, tmp_path: Path):
    audio_path = tmp_path / "note.wav"
    audio_path.write_bytes(b"fixture")
    calls: dict[str, object] = {}
    _install_whisper_double(monkeypatch, calls)

    transcript = SpeechToText(
        engine="whisper", model_size="base", allow_model_download=True
    ).transcribe_file(audio_path, language="en")

    assert transcript == "local transcript"
    assert calls["model_ref"] == "base"
    assert calls["transcribe"] == (str(audio_path), "en")


def test_whisper_accepts_explicit_local_model_file(monkeypatch, tmp_path: Path):
    audio_path = tmp_path / "note.wav"
    audio_path.write_bytes(b"fixture")
    model_path = tmp_path / "base.pt"
    model_path.write_bytes(b"model fixture")
    calls: dict[str, object] = {}
    _install_whisper_double(monkeypatch, calls)

    transcript = SpeechToText(engine="whisper", model_path=model_path).transcribe_file(audio_path)

    assert transcript == "local transcript"
    assert calls["model_ref"] == str(model_path)


def test_stt_existing_audio_reports_missing_optional_engine(monkeypatch, tmp_path: Path):
    audio_path = tmp_path / "note.wav"
    audio_path.write_bytes(b"not-a-real-audio-file")
    monkeypatch.setattr(stt_module, "find_spec", lambda name: None)

    with pytest.raises(RuntimeError, match="Install an optional STT extra"):
        SpeechToText().transcribe_file(audio_path)


def test_tts_requires_supported_extension(tmp_path: Path):
    with pytest.raises(ValueError):
        TextToSpeech().speak_to_file("hello", tmp_path / "speech.txt")


def test_tts_pyttsx3_routes_voice_and_wav_output_without_engine_import(monkeypatch, tmp_path: Path):
    calls: list[tuple] = []

    class FakeSpeaker:
        def getProperty(self, name: str):
            assert name == "voices"
            return [types.SimpleNamespace(name="Fixture Voice", id="fixture-id")]

        def setProperty(self, name: str, value):
            calls.append(("set", name, value))

        def save_to_file(self, text: str, path: str):
            calls.append(("save", text))
            Path(path).write_bytes(b"RIFF-fixture")

        def runAndWait(self):
            calls.append(("run",))

    speaker = FakeSpeaker()
    monkeypatch.setattr(TextToSpeech, "available", lambda self: (True, "pyttsx3"))
    monkeypatch.setattr(TextToSpeech, "_ensure_pyttsx3", lambda self: speaker)

    output = tmp_path / "reply.wav"
    result = TextToSpeech(engine="pyttsx3", voice_name="fixture").speak_to_file("hello", output)

    assert result == output
    assert output.read_bytes() == b"RIFF-fixture"
    assert ("set", "voice", "fixture-id") in calls
    assert ("save", "hello") in calls
    assert ("run",) in calls


def test_tts_piper_requires_model_before_optional_import(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(TextToSpeech, "available", lambda self: (True, "piper"))

    with pytest.raises(RuntimeError, match="explicit piper_model"):
        TextToSpeech(engine="piper").speak_to_file("hello", tmp_path / "reply.wav")

    with pytest.raises(FileNotFoundError):
        TextToSpeech(engine="piper", piper_model=tmp_path / "missing.onnx").speak_to_file(
            "hello", tmp_path / "reply.wav"
        )


def test_tts_non_wav_format_routes_through_ffmpeg(monkeypatch, tmp_path: Path):
    source = tmp_path / "source.wav"
    output = tmp_path / "reply.mp3"
    source.write_bytes(b"RIFF-fixture")
    calls: dict[str, object] = {}

    def fake_run(command, check, capture_output):
        calls["command"] = command
        calls["check"] = check
        calls["capture_output"] = capture_output
        output.write_bytes(b"mp3-fixture")

    monkeypatch.setattr(tts_module.subprocess, "run", fake_run)

    assert TextToSpeech._convert_or_copy(source, output) == output
    assert calls["command"][0] == "ffmpeg"
    assert calls["check"] is True
    assert calls["capture_output"] is True
    assert output.read_bytes() == b"mp3-fixture"


def test_wakeword_threshold_is_bounded():
    with pytest.raises(ValueError):
        WakeWordListener(0)
    with pytest.raises(ValueError):
        WakeWordListener(1.1)


def test_status_cli_is_read_only(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["ellmos-voice-io", "status"])
    assert main() == 0
    assert "stt_available" in capsys.readouterr().out


def _install_wakeword_doubles(monkeypatch, audio, model, stream):
    fake_numpy = types.SimpleNamespace(frombuffer=lambda data, dtype: data, int16=object())
    fake_pyaudio = types.SimpleNamespace(PyAudio=lambda: audio, paInt16="paInt16")
    fake_openwakeword = types.ModuleType("openwakeword")
    fake_openwakeword.__path__ = []
    fake_model_module = types.ModuleType("openwakeword.model")
    fake_model_module.Model = lambda: model

    monkeypatch.setattr(wakeword_module, "find_spec", lambda name: object())
    monkeypatch.setitem(sys.modules, "numpy", fake_numpy)
    monkeypatch.setitem(sys.modules, "pyaudio", fake_pyaudio)
    monkeypatch.setitem(sys.modules, "openwakeword", fake_openwakeword)
    monkeypatch.setitem(sys.modules, "openwakeword.model", fake_model_module)


def test_wakeword_repeated_hits_callback_contract_and_cleanup(monkeypatch):
    stop_event = threading.Event()
    callbacks: list[str] = []

    class FakeStream:
        def __init__(self):
            self.reads = 0
            self.stops = 0
            self.closes = 0

        def read(self, frames, exception_on_overflow):
            self.reads += 1
            return b"\x00" * frames

        def stop_stream(self):
            self.stops += 1

        def close(self):
            self.closes += 1

    class FakeModel:
        prediction_buffer = {"fixture": [0.9]}

        def predict(self, samples):
            return None

    stream = FakeStream()

    class FakeAudio:
        def __init__(self):
            self.terminated = 0

        def open(self, **kwargs):
            return stream

        def terminate(self):
            self.terminated += 1

    audio = FakeAudio()
    _install_wakeword_doubles(monkeypatch, audio, FakeModel(), stream)

    def on_wake():
        callbacks.append("wake")
        if len(callbacks) == 2:
            stop_event.set()

    WakeWordListener().listen(on_wake, stop_event)

    assert callbacks == ["wake", "wake"]
    assert stream.reads == 2
    assert stream.stops == 1
    assert stream.closes == 1
    assert audio.terminated == 1


def test_wakeword_pre_cancelled_event_skips_optional_engine_and_audio(monkeypatch):
    stop_event = threading.Event()
    stop_event.set()
    monkeypatch.setattr(WakeWordListener, "available", lambda self: pytest.fail("availability must not be queried"))

    WakeWordListener().listen(lambda: pytest.fail("callback must not run"), stop_event)


def test_wakeword_read_exception_cleans_stream_and_audio(monkeypatch):
    class FakeStream:
        stops = 0
        closes = 0

        def read(self, frames, exception_on_overflow):
            raise OSError("fixture read failed")

        def stop_stream(self):
            self.stops += 1

        def close(self):
            self.closes += 1

    class FakeModel:
        prediction_buffer = {}

        def predict(self, samples):
            return None

    class FakeAudio:
        def __init__(self):
            self.terminated = 0

        def open(self, **kwargs):
            return stream

        def terminate(self):
            self.terminated += 1

    stream = FakeStream()
    audio = FakeAudio()
    _install_wakeword_doubles(monkeypatch, audio, FakeModel(), stream)

    with pytest.raises(OSError, match="fixture read failed"):
        WakeWordListener().listen(lambda: None)

    assert stream.stops == 1
    assert stream.closes == 1
    assert audio.terminated == 1


def test_wakeword_callback_exception_cleans_stream_and_audio(monkeypatch):
    class FakeStream:
        stops = 0
        closes = 0

        def read(self, frames, exception_on_overflow):
            return b"\x00" * frames

        def stop_stream(self):
            self.stops += 1

        def close(self):
            self.closes += 1

    class FakeModel:
        prediction_buffer = {"fixture": [0.9]}

        def predict(self, samples):
            return None

    class FakeAudio:
        def __init__(self):
            self.terminated = 0

        def open(self, **kwargs):
            return stream

        def terminate(self):
            self.terminated += 1

    stream = FakeStream()
    audio = FakeAudio()
    _install_wakeword_doubles(monkeypatch, audio, FakeModel(), stream)

    with pytest.raises(RuntimeError, match="fixture callback failed"):
        WakeWordListener().listen(lambda: (_ for _ in ()).throw(RuntimeError("fixture callback failed")))

    assert stream.stops == 1
    assert stream.closes == 1
    assert audio.terminated == 1


def test_wakeword_open_exception_still_terminates_audio(monkeypatch):
    class FakeAudio:
        def __init__(self):
            self.terminated = 0

        def open(self, **kwargs):
            raise OSError("fixture open failed")

        def terminate(self):
            self.terminated += 1

    class FakeModel:
        prediction_buffer = {}

    audio = FakeAudio()
    _install_wakeword_doubles(monkeypatch, audio, FakeModel(), None)

    with pytest.raises(OSError, match="fixture open failed"):
        WakeWordListener().listen(lambda: None)

    assert audio.terminated == 1
