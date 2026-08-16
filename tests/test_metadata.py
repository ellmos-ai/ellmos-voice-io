import json
from pathlib import Path
import tomllib

import ellmos_voice_io


def test_version_parity():
    root = Path(__file__).resolve().parent.parent
    pyproject_path = root / "pyproject.toml"
    module_v2_path = root / "ellmos-module.v2.json"

    with pyproject_path.open("rb") as f:
        pyproject_data = tomllib.load(f)
    pyproject_version = pyproject_data["project"]["version"]

    with module_v2_path.open("r", encoding="utf-8") as f:
        module_v2_data = json.load(f)
    module_v2_version = module_v2_data["version"]

    assert ellmos_voice_io.__version__ == pyproject_version
    assert ellmos_voice_io.__version__ == module_v2_version


def test_module_v2_contract():
    root = Path(__file__).resolve().parent.parent
    module_v2_path = root / "ellmos-module.v2.json"

    with module_v2_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["schema"] == "ellmos.module.v2"
    assert data["id"] == "ellmos-voice-io"
    assert "provides" in data
    assert "surfaces" in data
    assert "entrypoints" in data
    assert data["entrypoints"]["cli"] == "ellmos-voice-io status"
    assert data["entrypoints"]["library"] == "ellmos_voice_io.VoiceIO"


def test_package_exports():
    expected_exports = ["SpeechToText", "TextToSpeech", "VoiceIO", "VoiceStatus", "WakeWordListener"]
    for export_name in expected_exports:
        assert hasattr(ellmos_voice_io, export_name)
        assert export_name in ellmos_voice_io.__all__
