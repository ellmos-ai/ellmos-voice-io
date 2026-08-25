import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_public_control_files_are_present():
    required = {
        ".github/workflows/ci.yml",
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        "RELEASE_GATE.md",
        "THIRD_PARTY_LICENSES.md",
        "TODO.md",
        "docs/ai-act-note.md",
    }
    missing = sorted(path for path in required if not (ROOT / path).is_file())
    assert not missing, f"missing public-readiness files: {missing}"

    ignore_lines = set((ROOT / ".gitignore").read_text(encoding="utf-8").splitlines())
    minimum_ignores = {"__pycache__/", "*.pyc", ".env", "*.db", ".venv/", ".idea/", ".vscode/", "data/"}
    assert minimum_ignores <= ignore_lines


def test_skill_version_matches_package_version():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    package_version = re.search(r'^version = "([^"]+)"$', pyproject, re.MULTILINE)
    skill_version = re.search(r"^version:\s*([^\s]+)$", skill, re.MULTILINE)
    assert package_version is not None
    assert skill_version is not None
    assert skill_version.group(1) == package_version.group(1)


def test_public_docs_contain_no_host_specific_development_paths():
    public_docs = [
        ROOT / "README.md",
        ROOT / "README_de.md",
        ROOT / "ROADMAP.md",
        ROOT / "SECURITY.md",
        ROOT / "llms.txt",
    ]
    forbidden = ("C:\\_Local_DEV", "C:\\Users\\", "C:/Users/", "OneDrive")
    for path in public_docs:
        text = path.read_text(encoding="utf-8")
        assert not any(marker in text for marker in forbidden), path.name


def test_ci_declares_all_supported_platforms():
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    for runner in ("ubuntu-latest", "windows-latest", "macos-latest"):
        assert runner in workflow
    for version in ('python-version: "3.10"', 'python-version: "3.11"', 'python-version: "3.12"'):
        assert version in workflow


def test_ci_actions_are_pinned_to_immutable_commits():
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    uses = re.findall(r"^\s*uses:\s*([^\s#]+)", workflow, re.MULTILINE)
    assert uses
    for action in uses:
        _name, separator, revision = action.rpartition("@")
        assert separator and re.fullmatch(r"[0-9a-f]{40}", revision), action


def test_readmes_keep_code_blocks_and_banner_in_sync():
    readme_en = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (ROOT / "README_de.md").read_text(encoding="utf-8")
    code_blocks_en = re.findall(r"```[^\n]*\n.*?```", readme_en, re.DOTALL)
    code_blocks_de = re.findall(r"```[^\n]*\n.*?```", readme_de, re.DOTALL)
    assert code_blocks_de == code_blocks_en
    assert "docs/assets/banner.png" in readme_en
    assert "docs/assets/banner.png" in readme_de


def test_third_party_inventory_calls_out_piper_copyleft():
    inventory = (ROOT / "THIRD_PARTY_LICENSES.md").read_text(encoding="utf-8")
    assert "piper-tts" in inventory
    assert "GPL-3.0-or-later" in inventory


def test_release_gate_records_unpublished_registry_state():
    gate = (ROOT / "RELEASE_GATE.md").read_text(encoding="utf-8")
    assert "PyPI" in gate
    assert "not published" in gate.lower()
    # GitHub visibility and PyPI publication are independent decisions: the
    # repository is public (owner decision F7=B, 2026-08-25) while the
    # package itself remains unpublished to PyPI. See RELEASE_GATE.md.
    assert "public" in gate.lower()
    assert "PUBLISHED" in gate
