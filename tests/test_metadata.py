import json
from pathlib import Path
import re

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

import ellmos_voice_io


def test_version_parity():
    root = Path(__file__).resolve().parent.parent
    pyproject_path = root / "pyproject.toml"
    module_v2_path = root / "ellmos-module.v2.json"
    llms_path = root / "llms.txt"
    readme_en_path = root / "README.md"
    readme_de_path = root / "README_de.md"

    with pyproject_path.open("rb") as f:
        pyproject_data = tomllib.load(f)
    pyproject_version = pyproject_data["project"]["version"]

    with module_v2_path.open("r", encoding="utf-8") as f:
        module_v2_data = json.load(f)
    module_v2_version = module_v2_data["version"]

    assert ellmos_voice_io.__version__ == pyproject_version
    assert ellmos_voice_io.__version__ == module_v2_version

    llms_txt = llms_path.read_text(encoding="utf-8")
    assert f"Version: {pyproject_version}" in llms_txt

    readme_en = readme_en_path.read_text(encoding="utf-8")
    readme_de = readme_de_path.read_text(encoding="utf-8")
    assert f"Version-{pyproject_version}" in readme_en
    assert f"Version-{pyproject_version}" in readme_de


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
    assert data["package"] is None
    assert data["boundaries"]["network"] == "optional"

    allowed_keys = {
        "schema",
        "id",
        "display_name",
        "version",
        "category",
        "kind",
        "status",
        "visibility",
        "description",
        "package",
        "entrypoints",
        "provides",
        "requires",
        "optional",
        "conflicts",
        "surfaces",
        "profiles",
        "state",
        "boundaries",
        "source_of_truth",
        "adapters",
    }
    assert set(data) <= allowed_keys
    assert set(data["boundaries"]) == {"network", "data", "platforms"}


def test_package_exports():
    expected_exports = ["SpeechToText", "TextToSpeech", "VoiceIO", "VoiceStatus", "WakeWordListener"]
    for export_name in expected_exports:
        assert hasattr(ellmos_voice_io, export_name)
        assert export_name in ellmos_voice_io.__all__


def test_security_policy_contract():
    root = Path(__file__).resolve().parent.parent
    security_file = root / "SECURITY.md"
    assert security_file.is_file(), "SECURITY.md must be present in repository root"

    content = security_file.read_text(encoding="utf-8")
    assert "Local-First" in content
    assert "Microphone Lifecycle" in content or "Mikrofon-Lebenszyklus" in content
    assert "security/advisories/new" in content
    assert "0.2.x" in content


def test_sibling_ecosystem_matrix():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")

    key_siblings = [
        "ellmos-core",
        "ellmos-scheduler",
        "clutch",
        "coma",
        "gardener",
        "prompt-evidence-collector",
        "lock-master",
        "ticket-master",
        "ellmos-controlcenter-mcp",
        "usb-podcast-studio",
        "companion-for-agy",
        "safe-start-for-codex",
        "DevCenter",
        "open-bricks",
    ]

    for tool in key_siblings:
        assert tool in readme_en, f"Missing sibling tool {tool} in README.md"
        assert tool in readme_de, f"Missing sibling tool {tool} in README_de.md"


def test_llms_txt_integrity():
    root = Path(__file__).resolve().parent.parent
    llms_file = root / "llms.txt"
    assert llms_file.is_file()

    content = llms_file.read_text(encoding="utf-8")
    assert "Last-checked: 2026-08-25" in content
    assert re.search(r"Test-suite:\s*\d+/\d+\s*passed", content) is not None
    assert "SECURITY.md" in content
    assert "README.md" in content
    assert "README_de.md" in content


def test_documentation_hygiene():
    root = Path(__file__).resolve().parent.parent
    doc_files = [
        root / "README.md",
        root / "README_de.md",
        root / "llms.txt",
        root / "SECURITY.md",
        root / "CHANGELOG.md",
        root / "ROADMAP.md",
        root / "RELEASE_GATE.md",
        root / "THIRD_PARTY_LICENSES.md",
        root / "docs" / "ai-act-note.md",
    ]

    for doc in doc_files:
        if not doc.is_file():
            continue
        text = doc.read_text(encoding="utf-8")
        assert "file:///" not in text, f"Found file:/// URI scheme in {doc.name}"
        assert "C:\\Users\\" not in text and "C:/Users/" not in text, f"Found private user path in {doc.name}"


def test_ci_concurrency_configuration():
    root = Path(__file__).resolve().parent.parent
    ci_workflow = (root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "concurrency:" in ci_workflow
    assert "cancel-in-progress: true" in ci_workflow


def test_project_urls_pep621():
    root = Path(__file__).resolve().parent.parent
    with (root / "pyproject.toml").open("rb") as f:
        pyproject_data = tomllib.load(f)
    urls = pyproject_data["project"]["urls"]
    assert "Homepage" in urls
    assert "Documentation" in urls
    assert "Issues" in urls
    assert "Security" in urls
    assert "Parent Organization" in urls
    assert "Umbrella Ecosystem" in urls
    assert urls["Parent Organization"] == "https://github.com/ellmos-ai"
    assert urls["Umbrella Ecosystem"] == "https://github.com/open-bricks"


def test_security_sla_and_contacts():
    root = Path(__file__).resolve().parent.parent
    security_file = (root / "SECURITY.md").read_text(encoding="utf-8")
    assert "48 hours" in security_file or "48 Stunden" in security_file
    assert "security@ellmos.ai" in security_file
    assert "support@lukasgeiger.com" in security_file
    assert "lukas@open-bricks.org" in security_file


def test_gitignore_hygiene_patterns():
    root = Path(__file__).resolve().parent.parent
    gitignore_text = (root / ".gitignore").read_text(encoding="utf-8")
    assert "*.sync-conflict-*" in gitignore_text
    assert ".ruff_cache/" in gitignore_text
    assert "*.tmp" in gitignore_text
