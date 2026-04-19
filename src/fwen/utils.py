"""
Utility functions for Flutter Clean CLI.
"""

import os
import subprocess
from pathlib import Path


def run_command(
    cmd: list[str],
    cwd: str | None = None,
    capture_output: bool = True,
) -> tuple[bool, str, str]:
    """
    Run a shell command.

    Returns (success, stdout, stderr).
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            check=False,
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def copy_file_with_substitution(
    src: Path,
    dest: Path,
    substitutions: dict[str, str],
) -> None:
    """Copy a file while performing variable substitutions."""
    dest.parent.mkdir(parents=True, exist_ok=True)

    content = src.read_text()
    for key, value in substitutions.items():
        content = content.replace(f"{{{{{key}}}}}", value)

    dest.write_text(content)


def copy_directory(
    src: Path,
    dest: Path,
    substitutions: dict[str, str],
    ignore_patterns: list[str] | None = None,
) -> None:
    """
    Copy a directory with substitutions.

    ignore_patterns: List of glob patterns to ignore (e.g., ["*.pyc", "__pycache__"])
    """
    for item in src.rglob("*"):
        if item.is_file():
            rel_path = item.relative_to(src)
            dest_file = dest / rel_path

            # Skip if matches ignore patterns
            if ignore_patterns:
                if any(item.match(pattern) for pattern in ignore_patterns):
                    continue

            copy_file_with_substitution(item, dest_file, substitutions)


def merge_pubspec_dependencies(
    pubspec_path: Path,
    dependencies: dict[str, str],
    dev_dependencies: dict[str, str],
) -> None:
    """Merge dependencies into existing pubspec.yaml."""
    import yaml

    with open(pubspec_path) as f:
        pubspec = yaml.safe_load(f)

    if "dependencies" not in pubspec:
        pubspec["dependencies"] = {}
    if "dev_dependencies" not in pubspec:
        pubspec["dev_dependencies"] = {}

    pubspec["dependencies"].update(dependencies)
    pubspec["dev_dependencies"].update(dev_dependencies)

    with open(pubspec_path, "w") as f:
        yaml.dump(pubspec, f, default_flow_style=False, sort_keys=False)


def get_flutter_executable() -> str:
    """Get the Flutter executable path."""
    flutter = os.environ.get("FLUTTER_ROOT", "")
    if flutter:
        return str(Path(flutter) / "bin" / "flutter")
    return "flutter"


def check_flutter_installed() -> tuple[bool, str]:
    """Check if Flutter is installed and accessible."""
    success, stdout, stderr = run_command(["flutter", "--version"])
    if success:
        return True, stdout
    return False, stderr or "Flutter not found in PATH"


def get_connected_devices() -> list[dict[str, str]]:
    """Get list of connected Flutter devices."""
    success, stdout, _ = run_command(["flutter", "devices"])
    if not success:
        return []

    devices = []
    lines = stdout.split("\n")
    for line in lines:
        if "•" in line and "•" != line.strip()[0]:
            parts = line.split("•")
            if len(parts) >= 3:
                devices.append({
                    "id": parts[1].strip(),
                    "name": parts[2].strip(),
                })

    return devices


def create_directory_structure(base_path: Path, structure: dict[str, list[str]]) -> None:
    """
    Create a directory structure from a nested dict.

    Example:
        {
            "lib": ["main.dart"],
            "lib/features": ["auth", "home"],
        }
    """
    for dir_path, items in structure.items():
        full_path = base_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)

        for item in items:
            item_path = full_path / item
            if "." in item:  # Likely a file
                item_path.parent.mkdir(parents=True, exist_ok=True)
                item_path.touch()
            else:  # Directory
                item_path.mkdir(parents=True, exist_ok=True)


def print_tree(directory: Path, max_depth: int = 3, prefix: str = "") -> None:
    """Print a directory tree structure."""
    if max_depth == 0:
        return

    try:
        items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
    except PermissionError:
        return

    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        print(f"{prefix}{current_prefix}{item.name}")

        if item.is_dir() and not item.name.startswith("."):
            next_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(item, max_depth - 1, next_prefix)


def validate_output_directory(path: Path) -> tuple[bool, str]:
    """Validate output directory for project creation."""
    if not path.exists():
        return True, ""

    if not path.is_dir():
        return False, "Path exists but is not a directory"

    # Check if directory is empty
    contents = list(path.iterdir())
    if contents:
        return False, f"Directory is not empty (contains {len(contents)} items)"

    return True, ""
