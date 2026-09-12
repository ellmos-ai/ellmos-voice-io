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
    assert "Last-checked: 2026-09-12" in content
    assert re.search(r"Test-suite:\s*56/56\s*passed", content) is not None
    assert "SECURITY.md" in content
    assert "README.md" in content
    assert "README_de.md" in content
    assert "MARKETING-LOG.txt" in content


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
        root / "MARKETING-LOG.txt",
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
    assert "Third-Party Licenses" in urls
    assert "Marketing-Log" in urls
    assert "LLM-Ready" in urls
    assert urls["Parent Organization"] == "https://github.com/ellmos-ai"
    assert urls["Umbrella Ecosystem"] == "https://github.com/open-bricks"


def test_security_sla_and_contacts():
    root = Path(__file__).resolve().parent.parent
    security_file = (root / "SECURITY.md").read_text(encoding="utf-8")
    assert "48 hours" in security_file or "48 Stunden" in security_file
    assert "security@ellmos.ai" in security_file
    assert "support@lukasgeiger.com" in security_file
    assert "lukas@open-bricks.org" in security_file
    assert "security@open-bricks.org" in security_file
    assert "5 business days" in security_file or "5 Werktagen" in security_file


def test_gitignore_hygiene_patterns():
    root = Path(__file__).resolve().parent.parent
    gitignore_text = (root / ".gitignore").read_text(encoding="utf-8")
    assert "*.sync-conflict-*" in gitignore_text
    assert ".ruff_cache/" in gitignore_text
    assert "*.tmp" in gitignore_text
    assert "LOCK.*" in gitignore_text
    assert "*.lock" in gitignore_text
    assert "*.bak" in gitignore_text


def test_quick_navigation_anchors_and_parity():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")

    assert "### Quick Navigation" in readme_en
    assert "### Schnellnavigation" in readme_de

    for i in range(1, 16):
        assert f"[{i}. " in readme_en, f"Missing Quick Nav item {i} in README.md"
        assert f"[{i}. " in readme_de, f"Missing Quick Nav item {i} in README_de.md"

    assert "[16. License, Attribution & German Documentation](README_de.md)" in readme_en
    assert "[16. Lizenz, Urheberrecht & Englische Dokumentation](README.md)" in readme_de


def test_governance_invariants_table():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")

    assert "## 4. Safety Model & Governance Invariants" in readme_en
    assert "## 4. Sicherheitsmodell & Governance-Invarianten" in readme_de

    for num in range(1, 11):
        assert f"| {num} |" in readme_en, f"Missing invariant #{num} in README.md"
        assert f"| {num} |" in readme_de, f"Missing invariant #{num} in README_de.md"

    assert "Zero-Egress" in readme_en and "Zero-Egress" in readme_de
    assert "RunAsInvoker" in readme_en and "RunAsInvoker" in readme_de


def test_dual_mermaid_diagrams():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")

    for doc in (readme_en, readme_de):
        assert "```mermaid\ngraph TD" in doc
        assert "```mermaid\nsequenceDiagram" in doc
        assert "autonumber" in doc


def test_local_marketing_log_present():
    root = Path(__file__).resolve().parent.parent
    log_file = root / "MARKETING-LOG.txt"
    assert log_file.is_file(), "Missing MARKETING-LOG.txt"
    text = log_file.read_text(encoding="utf-8")
    assert len(text) > 200
    assert "MARKETING & DISCOVERABILITY LOG: ellmos-voice-io" in text
    assert "Pfad B" in text


def test_extended_sibling_matrix_coverage():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")

    additional_siblings = [
        "ellmos-clatcher-mcp",
        "n8n-manager-mcp",
        "skills",
        "automizer-for-claude-desktop",
        "WikiStub-Seed",
        "automation-master",
        "WinStorePackager",
    ]
    for tool in additional_siblings:
        assert tool in readme_en, f"Missing extended sibling {tool} in README.md"
        assert tool in readme_de, f"Missing extended sibling {tool} in README_de.md"


def test_ci_workflow_bytecode_compilation_gate():
    root = Path(__file__).resolve().parent.parent
    ci_workflow = (root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "python -m compileall -q src tests" in ci_workflow


def test_pyproject_python313_and_options():
    root = Path(__file__).resolve().parent.parent
    with (root / "pyproject.toml").open("rb") as f:
        data = tomllib.load(f)
    classifiers = data["project"]["classifiers"]
    assert "Programming Language :: Python :: 3.13" in classifiers
    pytest_opts = data.get("tool", {}).get("pytest", {}).get("ini_options", {})
    assert "-ra" in pytest_opts.get("addopts", "")
    assert "-v" in pytest_opts.get("addopts", "")


def test_ci_matrix_expanded_python_coverage():
    root = Path(__file__).resolve().parent.parent
    ci_workflow = (root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    for os_name in ("ubuntu-latest", "windows-latest", "macos-latest"):
        for py_ver in ("3.10", "3.11", "3.12", "3.13"):
            pattern = rf"- os: {re.escape(os_name)}\s+python-version: \"{re.escape(py_ver)}\""
            assert re.search(pattern, ci_workflow) is not None, f"Missing matrix job {os_name} / {py_ver}"


def test_gitignore_multihost_and_lock_patterns():
    root = Path(__file__).resolve().parent.parent
    gitignore_text = (root / ".gitignore").read_text(encoding="utf-8")
    patterns = [
        "*-WORKSTATION-LG.*",
        "*-WORKSTATION-LG-*",
        "*-ASUS-GEI.*",
        "*-ASUS-GEI-*",
        "Thumbs.db",
        "desktop.ini",
        "* (kopie)*",
        "* (copy)*",
        "LOCK",
        "LOCK*",
        "*.orig",
        "*.rej",
        ".cache/",
    ]
    for pattern in patterns:
        assert pattern in gitignore_text, f"Missing pattern {pattern} in .gitignore"


def test_clean_bytecode_compilation():
    import compileall
    root = Path(__file__).resolve().parent.parent
    assert compileall.compile_dir(str(root / "src"), force=False, quiet=1)
    assert compileall.compile_dir(str(root / "tests"), force=False, quiet=1)


def test_license_files_metadata_contract():
    root = Path(__file__).resolve().parent.parent
    with (root / "pyproject.toml").open("rb") as f:
        data = tomllib.load(f)
    assert data["project"]["license"] == "MIT"
    license_files = data["project"]["license-files"]
    assert "LICENSE" in license_files
    assert "THIRD_PARTY_LICENSES.md" in license_files
    for lf in license_files:
        p = root / lf
        assert p.is_file(), f"Missing license file {lf}"
        assert len(p.read_text(encoding="utf-8").strip()) > 50


def test_target_personas_and_discoverability_contract():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")
    mkt_log = (root / "MARKETING-LOG.txt").read_text(encoding="utf-8")

    assert "## 10. Target Personas & Discoverability" in readme_en
    assert "## 10. Zielgruppen & Auffindbarkeit" in readme_de

    personas = [
        "Autonomous Local AI Agent Developers",
        "Privacy-Conscious Desktop Application Engineers",
        "Edge & Embedded AI Engineers",
        "Enterprise Security",
    ]
    for persona in personas:
        assert persona in readme_en, f"Missing persona '{persona}' in README.md"
        assert persona in mkt_log, f"Missing persona '{persona}' in MARKETING-LOG.txt"


def test_third_party_licenses_audit_contract():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")
    lic_file = (root / "THIRD_PARTY_LICENSES.md").read_text(encoding="utf-8")

    assert "## 11. Third-Party Licenses & Dependency Audits" in readme_en
    assert "## 11. Drittanbieter-Lizenzen & Abhängigkeits-Audits" in readme_de

    assert "piper-tts" in lic_file
    assert "GPL-3.0-or-later" in lic_file
    assert "zero external runtime dependencies" in lic_file.lower()


def test_competitive_matrix_and_invariants_in_marketing_log():
    root = Path(__file__).resolve().parent.parent
    mkt_log = (root / "MARKETING-LOG.txt").read_text(encoding="utf-8")

    assert "COMPETITIVE DIFFERENTIATION MATRIX" in mkt_log
    competitors = ["Cloud APIs", "SpeechRecognition", "WhisperX", "PyAudio"]
    for comp in competitors:
        assert comp in mkt_log, f"Missing competitor keyword '{comp}' in MARKETING-LOG.txt"

    for inv_num in range(1, 11):
        assert f"{inv_num:02d}" in mkt_log


def test_policy_registry_sibling_coverage():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")

    assert "policy-registry" in readme_en
    assert "policy-registry" in readme_de


def test_zero_runtime_dependencies_and_optional_extras():
    root = Path(__file__).resolve().parent.parent
    with (root / "pyproject.toml").open("rb") as f:
        data = tomllib.load(f)
    assert data["project"]["dependencies"] == [], "Base wheel must have zero runtime dependencies"
    optional = data["project"]["optional-dependencies"]
    expected_extras = ["stt-vosk", "stt-whisper", "tts-pyttsx3", "tts-piper", "wakeword", "all"]
    for extra in expected_extras:
        assert extra in optional, f"Missing expected extra '{extra}' in optional-dependencies"
