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
    assert "Last-checked: 2026-09-23" in content
    assert re.search(r"Test-suite:\s*\d+/\d+\s*passed", content) is not None
    assert "NOTICE" in content
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
        root / "ROADMAP.md",
        root / "RELEASE_GATE.md",
        root / "THIRD_PARTY_LICENSES.md",
        root / "docs" / "ai-act-note.md",
    ]
    for doc in doc_files:
        assert doc.is_file(), f"Missing doc file {doc}"
        text = doc.read_text(encoding="utf-8")
        assert len(text.strip()) > 100, f"Doc file {doc} appears suspiciously short"
        assert "TODO" not in text, f"Unresolved TODO found in {doc}"


def test_roadmap_contract():
    root = Path(__file__).resolve().parent.parent
    roadmap_path = root / "ROADMAP.md"
    assert roadmap_path.is_file()

    content = roadmap_path.read_text(encoding="utf-8")
    assert "Completed gates" in content or "Remaining external gates" in content
    assert "RELEASE_GATE.md" in content


def test_release_gate_contract():
    root = Path(__file__).resolve().parent.parent
    rg_path = root / "RELEASE_GATE.md"
    assert rg_path.is_file()

    content = rg_path.read_text(encoding="utf-8")
    assert "PyPI" in content
    assert "Registry" in content or "Owner" in content


def test_security_sla_and_contacts():
    root = Path(__file__).resolve().parent.parent
    security_file = root / "SECURITY.md"
    content = security_file.read_text(encoding="utf-8")

    assert "48" in content, "Missing 48-hour response commitment in SECURITY.md"
    assert "security@open-bricks.org" in content
    assert "security@ellmos.ai" in content


def test_project_urls_pep621():
    root = Path(__file__).resolve().parent.parent
    with (root / "pyproject.toml").open("rb") as f:
        data = tomllib.load(f)

    urls = data.get("project", {}).get("urls", {})
    expected_keys = [
        "Homepage",
        "Documentation",
        "Issues",
        "Security",
        "Parent Organization",
        "Umbrella Ecosystem",
        "Third-Party Licenses",
        "Marketing-Log",
        "LLM-Ready",
    ]
    for key in expected_keys:
        assert key in urls, f"Missing URL key '{key}' in pyproject.toml"
        assert urls[key].startswith("http"), f"URL for '{key}' is invalid"


def test_quick_navigation_anchors_and_parity():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")

    assert "### 🧭 Quick Navigation" in readme_en
    assert "### 🧭 Schnellnavigation" in readme_de

    for i in range(1, 19):
        assert f"[{i}. " in readme_en or f"{i}. [" in readme_en, f"Missing Quick Nav item {i} in README.md"
        assert f"[{i}. " in readme_de or f"{i}. [" in readme_de, f"Missing Quick Nav item {i} in README_de.md"

    assert "(#license)" in readme_en
    assert "(#lizenz)" in readme_de


def test_bilingual_readme_navigation_parity():
    """Verify that README.md and README_de.md have full 18-point quick navigation parity and heading targets."""
    root = Path(__file__).resolve().parent.parent
    en_content = (root / "README.md").read_text(encoding="utf-8")
    de_content = (root / "README_de.md").read_text(encoding="utf-8")

    en_anchors = [
        "#executive-summary--core-identity",
        "#visual-architecture-topology",
        "#audio-lifecycle--event-flow",
        "#safety-model--governance-invariants",
        "#comparative-matrix-vs-alternatives",
        "#marketing--target-personas",
        "#scope--supported-engines",
        "#installation--environment-setup",
        "#read-only-cli-operations",
        "#python-api",
        "#privacy-and-hardware-boundaries",
        "#third-party-licenses--transparency",
        "#ecosystem--sibling-tools",
        "#development-status--roadmap",
        "#provenance--history-boundary",
        "#security-policy",
        "#testing-verification--quality-gates",
        "#license",
    ]

    de_anchors = [
        "#management-zusammenfassung--kernidentitaet",
        "#visuelle-architektur-topologie",
        "#audio-lebenszyklus--ereignisfluss",
        "#sicherheitsmodell--governance-invarianten",
        "#vergleichsmatrix-gegenueber-alternativen",
        "#marketing--zielgruppen",
        "#umfang--unterstuetzte-engines",
        "#installation--umgebungseinrichtung",
        "#rein-lesende-cli-bedienung",
        "#python-api",
        "#datenschutz-und-hardware-grenzen",
        "#drittanbieter-lizenzen--transparenz",
        "#oekosystem--geschwisterwerkzeuge",
        "#entwicklungsstatus--roadmap",
        "#provenienz--historien-grenze",
        "#sicherheitsrichtlinie",
        "#tests-ausfuehren",
        "#lizenz",
    ]

    assert len(en_anchors) == 18
    assert len(de_anchors) == 18

    for anchor in en_anchors:
        assert f"({anchor})" in en_content, f"Anchor {anchor} missing in README.md Quick Navigation"
        anchor_id = anchor.lstrip("#")
        assert f'id="{anchor_id}"' in en_content, f'Target id="{anchor_id}" missing in README.md headings'

    for anchor in de_anchors:
        assert f"({anchor})" in de_content, f"Anchor {anchor} missing in README_de.md Schnellnavigation"
        anchor_id = anchor.lstrip("#")
        assert f'id="{anchor_id}"' in de_content, f'Target id="{anchor_id}" missing in README_de.md headings'


def test_governance_invariants_table():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")

    assert "Safety Model & Governance Invariants" in readme_en
    assert "Sicherheitsmodell & Governance-Invarianten" in readme_de

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
        assert "```mermaid\nflowchart TD" in doc
        assert "```mermaid\nsequenceDiagram" in doc
        assert "autonumber" in doc


def test_dual_mermaid_diagrams_and_semicolons_free():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")

    for doc in (readme_en, readme_de):
        mermaid_blocks = re.findall(r"```mermaid\s+(.*?)\s+```", doc, re.DOTALL)
        assert len(mermaid_blocks) >= 2, "Must contain at least 2 mermaid diagrams"
        for block in mermaid_blocks:
            for line in block.splitlines():
                line_clean = line.strip()
                if line_clean and not line_clean.startswith("%%") and not line_clean.startswith("note"):
                    assert not line_clean.endswith(";"), f"Mermaid line ends with illegal semicolon: '{line_clean}'"


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
    assert "NOTICE" in license_files
    assert "THIRD_PARTY_LICENSES.md" in license_files
    for lf in license_files:
        p = root / lf
        assert p.is_file(), f"Missing license file {lf}"
        assert len(p.read_text(encoding="utf-8").strip()) > 50


def test_notice_attribution_file():
    root = Path(__file__).resolve().parent.parent
    notice = root / "NOTICE"
    assert notice.is_file(), "NOTICE file must exist in repository root"
    content = notice.read_text(encoding="utf-8")
    assert "ellmos-voice-io" in content
    assert "Lukas Geiger" in content
    assert "ellmos-ai" in content
    assert "open-bricks" in content
    assert "MIT License" in content


def test_target_personas_and_discoverability_contract():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")
    mkt_log = (root / "MARKETING-LOG.txt").read_text(encoding="utf-8")

    assert "Target Personas" in readme_en
    assert "Zielgruppen" in readme_de

    personas = [
        "Autonomous Local AI Agent Developers",
        "Privacy-Conscious Desktop Application Engineers",
        "Edge & Embedded AI Engineers",
        "Enterprise Security",
    ]
    for persona in personas:
        assert persona in readme_en, f"Missing persona '{persona}' in README.md"
        assert persona in mkt_log, f"Missing persona '{persona}' in MARKETING-LOG.txt"

    for tag in ["[PERSONA-01]", "[PERSONA-02]", "[PERSONA-03]", "[PERSONA-04]"]:
        assert tag in readme_en, f"Missing persona tag '{tag}' in README.md"
        assert tag in readme_de, f"Missing persona tag '{tag}' in README_de.md"
        assert tag in mkt_log, f"Missing persona tag '{tag}' in MARKETING-LOG.txt"


def test_third_party_licenses_audit_contract():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")
    lic_file = (root / "THIRD_PARTY_LICENSES.md").read_text(encoding="utf-8")

    assert "Third-Party Licenses" in readme_en
    assert "Drittanbieter-Lizenzen" in readme_de

    assert "piper-tts" in lic_file
    assert "GPL-3.0-or-later" in lic_file
    assert "zero external runtime dependencies" in lic_file.lower()
    assert "Level 1 Software Bill of Materials (SBOM)" in lic_file


def test_level1_sbom_and_cross_reference_matrix():
    root = Path(__file__).resolve().parent.parent
    third_party = (root / "THIRD_PARTY_LICENSES.md").read_text(encoding="utf-8")

    assert "Level 1 Software Bill of Materials (SBOM)" in third_party
    assert "Invariant Cross-Reference Matrix" in third_party
    assert "RunAsInvoker" in third_party
    assert "Zero-Copyleft Isolation Guarantee" in third_party

    invariants = [
        "INV-LOCAL-01",
        "INV-SEC-02",
        "INV-CONSENT-03",
        "INV-MIC-04",
        "INV-DATA-05",
        "INV-LAZY-06",
        "INV-CLI-07",
        "INV-PORT-08",
        "INV-SYNC-09",
        "INV-SLA-10",
    ]
    for inv in invariants:
        assert inv in third_party, f"Missing invariant {inv} in THIRD_PARTY_LICENSES.md"


def test_comparative_matrix_sections():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")

    assert "Comparative Matrix vs. Alternatives" in readme_en
    assert "Vergleichsmatrix gegenüber Alternativen" in readme_de

    alternatives = [
        "Cloud Speech APIs",
        "SpeechRecognition",
        "WhisperX",
        "PyAudio",
    ]
    for alt in alternatives:
        assert alt in readme_en, f"Missing alternative {alt} in README.md"

    de_alternatives = [
        "Cloud-Sprach-APIs",
        "SpeechRecognition",
        "WhisperX",
        "PyAudio",
    ]
    for alt in de_alternatives:
        assert alt in readme_de, f"Missing alternative {alt} in README_de.md"


def test_statutory_disclaimer_521_bgb():
    root = Path(__file__).resolve().parent.parent
    readme_en = (root / "README.md").read_text(encoding="utf-8")
    readme_de = (root / "README_de.md").read_text(encoding="utf-8")

    assert "§ 521 BGB" in readme_en
    assert "§ 521 BGB" in readme_de
    assert "Vorsatz und grobe Fahrlässigkeit" in readme_en
    assert "Vorsatz und grobe Fahrlässigkeit" in readme_de
    assert "Gefälligkeit" in readme_en
    assert "Gefälligkeit" in readme_de


def test_governance_invariants_parity():
    root = Path(__file__).resolve().parent.parent
    invariants = [
        "INV-LOCAL-01",
        "INV-SEC-02",
        "INV-CONSENT-03",
        "INV-MIC-04",
        "INV-DATA-05",
        "INV-LAZY-06",
        "INV-CLI-07",
        "INV-PORT-08",
        "INV-SYNC-09",
        "INV-SLA-10",
    ]
    for target in ("README.md", "README_de.md", "THIRD_PARTY_LICENSES.md", "llms.txt"):
        content = (root / target).read_text(encoding="utf-8")
        for inv in invariants:
            assert inv in content, f"Invariant {inv} missing in {target}"


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


def test_ci_workflow_timeout_minutes():
    root = Path(__file__).resolve().parent.parent
    ci_workflow = (root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "timeout-minutes: 15" in ci_workflow


def test_stale_workflow_contract():
    root = Path(__file__).resolve().parent.parent
    stale_workflow_path = root / ".github" / "workflows" / "stale.yml"
    assert stale_workflow_path.is_file(), "Missing .github/workflows/stale.yml"
    content = stale_workflow_path.read_text(encoding="utf-8")
    assert "actions/stale@v9" in content
    assert "timeout-minutes: 10" in content
    assert "issues: write" in content
    assert "pull-requests: write" in content


def test_gitignore_cloud_sync_and_lock_defense():
    root = Path(__file__).resolve().parent.parent
    gitignore_text = (root / ".gitignore").read_text(encoding="utf-8")
    required_patterns = [
        "*conflicted copy*",
        "*-LAPTOP.*",
        "*-LAPTOP-*",
        "uv.lock",
        "poetry.lock",
        "!package-lock.json",
    ]
    for pattern in required_patterns:
        assert pattern in gitignore_text, f"Missing pattern {pattern} in .gitignore"


def test_welcome_workflow_contract():
    root = Path(__file__).resolve().parent.parent
    welcome_path = root / ".github" / "workflows" / "welcome.yml"
    assert welcome_path.is_file(), "Missing .github/workflows/welcome.yml"
    content = welcome_path.read_text(encoding="utf-8")
    assert "actions/first-interaction@v3" in content
    assert "timeout-minutes: 5" in content
    assert "issues: write" in content
    assert "pull-requests: write" in content
    assert "cancel-in-progress: true" in content


def test_stale_workflow_concurrency_hardened():
    root = Path(__file__).resolve().parent.parent
    stale_path = root / ".github" / "workflows" / "stale.yml"
    assert stale_path.is_file()
    content = stale_path.read_text(encoding="utf-8")
    assert "cancel-in-progress: true" in content
    assert "group: stale-" in content


def test_extended_multihost_and_lock_defense():
    root = Path(__file__).resolve().parent.parent
    gitignore_text = (root / ".gitignore").read_text(encoding="utf-8")
    patterns = [
        "* (Kopie)*",
        "* (Copy)*",
        "*-ASUS*",
        "*-LAPTOP*",
        "*-Mac Studio*",
        "*-MacBook*",
        "LOCK.user.*",
        "LOCK.until.*",
        "LOCK.condition.*",
        ".automation-lock",
        ".pytest_temp/",
        ".pytest_tmp*/",
        ".hypothesis/",
        ".turbo/",
        ".nyc_output/",
    ]
    for pattern in patterns:
        assert pattern in gitignore_text, f"Missing pattern {pattern} in .gitignore"


def test_pytest_basetemp_and_norecursedirs_hardening():
    root = Path(__file__).resolve().parent.parent
    with (root / "pyproject.toml").open("rb") as f:
        data = tomllib.load(f)
    pytest_opts = data.get("tool", {}).get("pytest", {}).get("ini_options", {})
    addopts = pytest_opts.get("addopts", "")
    assert "--basetemp=.pytest_temp" in addopts
    norecurse = pytest_opts.get("norecursedirs", [])
    assert ".pytest_temp" in norecurse


def test_pep621_notice_url():
    root = Path(__file__).resolve().parent.parent
    with (root / "pyproject.toml").open("rb") as f:
        data = tomllib.load(f)
    urls = data.get("project", {}).get("urls", {})
    assert "Notice" in urls
    assert urls["Notice"] == "https://github.com/ellmos-ai/ellmos-voice-io/blob/main/NOTICE"


def test_changelog_unreleased_pfad_a_entry():
    root = Path(__file__).resolve().parent.parent
    changelog_text = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [Unreleased]" in changelog_text
    assert "Pfad A - 2026-09-23" in changelog_text
    assert "welcome.yml" in changelog_text
    assert "stale.yml" in changelog_text
    assert "Multi-Host" in changelog_text
    assert "basetemp" in changelog_text


def test_marketing_log_recent_pfad_a_entry():
    root = Path(__file__).resolve().parent.parent
    mkt_text = (root / "MARKETING-LOG.txt").read_text(encoding="utf-8")
    assert "Date: 2026-09-23" in mkt_text
    assert "PFAD A AUDIT 2026-09-23" in mkt_text
    assert "welcome.yml" in mkt_text
    assert "LOCK.user.*" in mkt_text
    assert "--basetemp=.pytest_temp" in mkt_text
