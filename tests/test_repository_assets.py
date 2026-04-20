"""Repository-level tests for packaged assets and scripts."""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from fwen.template_registry import get_implemented_templates  # noqa: E402


class TestRepositoryAssets(unittest.TestCase):
    """Verify repository assets needed by the CLI are present."""

    def test_templates_directory_contains_required_implemented_entries(self):
        """Implemented templates declared in the registry must exist in the repository."""
        templates_dir = REPO_ROOT / "templates"

        for template in get_implemented_templates():
            required_path = templates_dir / template.source_path
            self.assertTrue(
                required_path.exists(),
                f"Missing required implemented template: {template.template_id} ({required_path})",
            )

    def test_feature_templates_use_double_brace_placeholders(self):
        """Feature templates should use the repository's substitution format."""
        feature_template = REPO_ROOT / "templates" / "feature" / "entity.dart"
        manager_template = REPO_ROOT / "templates" / "feature" / "manager.dart"
        content = feature_template.read_text()
        manager_content = manager_template.read_text()

        self.assertIn("{{FeatureName}}", content)
        self.assertIn("{{FeatureName}}", manager_content)
        self.assertIn("{{feature_name}}", manager_content)

    def test_commerce_reference_templates_use_project_placeholders(self):
        """Commerce scenario templates should preserve project substitution placeholders."""
        routes_template = (
            REPO_ROOT
            / "templates"
            / "scenarios"
            / "commerce_reference"
            / "lib"
            / "app"
            / "routes.dart"
        )
        auth_usecase_template = (
            REPO_ROOT
            / "templates"
            / "scenarios"
            / "commerce_reference"
            / "lib"
            / "features"
            / "auth"
            / "domain"
            / "usecases"
            / "get_signed_in_user_usecase.dart"
        )

        self.assertIn("{{ProjectName}}", routes_template.read_text())
        self.assertIn("{{project_name}}", auth_usecase_template.read_text())

    def test_feature_script_uses_repo_templates(self):
        """The feature script should resolve routes from the current repo templates."""
        script_path = REPO_ROOT / "scripts" / "feature-dev.py"
        content = script_path.read_text()

        self.assertIn('"base/lib/app/routes.dart"', content)
        self.assertNotIn("flutter-clean-app-creator", content)

    def test_feature_script_routes_template_exists(self):
        """The routes template expected by the feature script should exist."""
        routes_template = REPO_ROOT / "templates" / "base" / "lib" / "app" / "routes.dart"
        self.assertTrue(routes_template.exists())

    def test_base_app_shell_templates_are_wired_for_di_and_state(self):
        """The base app shell should expose DI, shared state, and routing wiring."""
        app_template = REPO_ROOT / "templates" / "base" / "lib" / "app" / "app.dart"
        home_page_template = (
            REPO_ROOT / "templates" / "base" / "lib" / "app" / "pages" / "home_page.dart"
        )
        bootstrap_template = REPO_ROOT / "templates" / "base" / "lib" / "bootstrap.dart"
        state_template = (
            REPO_ROOT
            / "templates"
            / "base"
            / "lib"
            / "core"
            / "state_management"
            / "app_state.dart"
        )

        self.assertIn("AppStateScope", app_template.read_text())
        self.assertIn("buildAppRouter", app_template.read_text())
        self.assertIn("configureDependencies", bootstrap_template.read_text())
        self.assertIn("configureStateManagement", bootstrap_template.read_text())
        self.assertIn("AppStateScope.of(context)", home_page_template.read_text())
        self.assertIn("class AppStateController", state_template.read_text())


if __name__ == "__main__":
    unittest.main()
