"""
Project generator module for Flutter Clean CLI.
Handles Flutter project creation and template application.
"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional

from .config import Config
from .utils import (
    copy_directory,
    copy_file_with_substitution,
    get_flutter_executable,
    merge_pubspec_dependencies,
    run_command,
)


class ProjectGenerator:
    """Generates Flutter projects with Clean Architecture."""

    def __init__(self, config: Config, templates_dir: Path):
        """Initialize generator with config and templates directory."""
        self.config = config
        self.templates_dir = templates_dir
        self.project_path: Optional[Path] = None

    def generate(self) -> tuple[bool, str]:
        """
        Generate the Flutter project.

        Returns (success, message).
        """
        project_name = self.config.get("project_name")
        output_dir = Path(self.config.get("output_dir", "."))

        # Create output directory if it doesn't exist
        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)

        # Step 1: Create Flutter project
        success, message = self._create_flutter_project()
        if not success:
            return False, message

        # Set project path after successful creation
        self.project_path = output_dir / project_name

        # Step 2: Apply templates
        success, message = self._apply_templates()
        if not success:
            return False, message

        # Step 3: Update pubspec.yaml
        success, message = self._update_pubspec()
        if not success:
            return False, message

        # Step 4: Create initial feature if requested
        if self.config.get("create_feature"):
            success, message = self._create_initial_feature()
            if not success:
                return False, message

        return True, f"Project created at {self.project_path}"

    def _create_flutter_project(self) -> tuple[bool, str]:
        """Create base Flutter project using flutter create."""
        project_name = self.config.get("project_name")
        org_id = self.config.get("org_id", "com.example")
        platforms = self.config.get_selected_platforms()

        cmd = [get_flutter_executable(), "create", "--org", org_id]

        # Add platform flags
        for platform in platforms:
            cmd.extend(["--platforms", platform])

        cmd.append(project_name)

        success, stdout, stderr = run_command(
            cmd,
            cwd=self.config.get("output_dir", "."),
            capture_output=False,
        )

        if not success:
            return False, f"Failed to create Flutter project: {stderr}"

        return True, "Flutter project created"

    def _apply_templates(self) -> tuple[bool, str]:
        """Apply template files to the project."""
        if not self.project_path:
            return False, "Project path not set"

        substitutions = self.config.get_substitution_vars()

        # Remove default lib directory
        lib_dir = self.project_path / "lib"
        if lib_dir.exists():
            shutil.rmtree(lib_dir)

        # Apply base templates
        base_templates = self.templates_dir / "base"
        if base_templates.exists():
            copy_directory(base_templates, self.project_path, substitutions)

        # Apply state management templates
        sm = self.config.get("state_management")
        sm_templates = self.templates_dir / "state_management" / sm
        if sm_templates.exists():
            # Merge into lib directory
            copy_directory(
                sm_templates,
                self.project_path / "lib",
                substitutions,
            )

        # Apply navigation templates
        nav = self.config.get("navigation")
        nav_templates = self.templates_dir / "navigation" / nav
        if nav_templates.exists():
            copy_directory(nav_templates, self.project_path / "lib", substitutions)

        # Apply Firebase templates if enabled
        if self.config.get("include_firebase"):
            firebase_templates = self.templates_dir / "firebase"
            if firebase_templates.exists():
                services = self.config.get_selected_firebase_services()
                for service in services:
                    service_templates = firebase_templates / service
                    if service_templates.exists():
                        copy_directory(service_templates, self.project_path, substitutions)

        # Apply testing templates if enabled
        if self.config.get("include_testing"):
            testing_templates = self.templates_dir / "testing"
            if testing_templates.exists():
                copy_directory(testing_templates, self.project_path, substitutions)

        return True, "Templates applied"

    def _update_pubspec(self) -> tuple[bool, str]:
        """Update pubspec.yaml with selected dependencies."""
        if not self.project_path:
            return False, "Project path not set"

        pubspec_path = self.project_path / "pubspec.yaml"
        if not pubspec_path.exists():
            return False, "pubspec.yaml not found"

        deps = self.config.get_pubspec_dependencies()
        merge_pubspec_dependencies(
            pubspec_path,
            deps["dependencies"],
            deps["dev_dependencies"],
        )

        return True, "pubspec.yaml updated"

    def _create_initial_feature(self) -> tuple[bool, str]:
        """Create the initial feature module."""
        if not self.project_path:
            return False, "Project path not set"

        feature_name = self.config.get("feature_name")
        if not feature_name:
            return True, "No feature to create"

        # Use existing feature-dev.py script
        feature_script = self.templates_dir.parent / "scripts" / "feature-dev.py"
        if not feature_script.exists():
            return False, "feature-dev.py script not found"

        success, stdout, stderr = run_command(
            ["python3", str(feature_script), feature_name],
            cwd=str(self.project_path),
        )

        if not success:
            return False, f"Failed to create feature: {stderr}"

        return True, f"Feature '{feature_name}' created"

    def get_project_path(self) -> Path:
        """Get the generated project path."""
        return self.project_path or Path()


def generate_project(config: Config, templates_dir: Path) -> tuple[bool, str, Optional[Path]]:
    """
    Generate a Flutter project with the given configuration.

    Returns (success, message, project_path).
    """
    generator = ProjectGenerator(config, templates_dir)
    success, message = generator.generate()

    return success, message, generator.get_project_path()
