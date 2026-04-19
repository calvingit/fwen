"""Repository-level tests for packaged assets and scripts."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


class TestRepositoryAssets(unittest.TestCase):
    """Verify repository assets needed by the CLI are present."""

    def test_templates_directory_contains_required_entries(self):
        """The packaged templates tree should contain the required base assets."""
        templates_dir = REPO_ROOT / "templates"

        required_paths = [
            templates_dir / "base" / "lib" / "main.dart",
            templates_dir / "base" / "lib" / "bootstrap.dart",
            templates_dir / "base" / "lib" / "app" / "app.dart",
            templates_dir / "base" / "lib" / "app" / "routes.dart",
            templates_dir / "base" / "lib" / "app" / "pages" / "home_page.dart",
            templates_dir / "base" / "lib" / "core" / "di" / "service_locator.dart",
            templates_dir / "base" / "lib" / "core" / "state_management" / "app_state.dart",
            templates_dir / "base" / "lib" / "shared" / "themes" / "app_theme.dart",
            templates_dir / "feature" / "entity.dart",
            templates_dir / "feature" / "page.dart",
            templates_dir / "auth" / "lib" / "features" / "auth" / "domain" / "entities" / "user_entity.dart",
            templates_dir / "api" / "lib" / "core" / "network" / "api_client.dart",
            templates_dir / "persistence" / "lib" / "core" / "storage" / "local_storage.dart",
            templates_dir / "analytics" / "lib" / "core" / "analytics" / "app_analytics.dart",
            templates_dir / "testing" / "test" / "widget" / "app_smoke_test.dart",
            templates_dir / "firebase" / "auth" / "lib" / "core" / "firebase" / "firebase_auth_service.dart",
        ]

        for required_path in required_paths:
            self.assertTrue(required_path.exists(), f"Missing required asset: {required_path}")

    def test_feature_templates_use_double_brace_placeholders(self):
        """Feature templates should use the repository's substitution format."""
        feature_template = REPO_ROOT / "templates" / "feature" / "entity.dart"
        content = feature_template.read_text()

        self.assertIn("{{FeatureName}}", content)

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
        home_page_template = REPO_ROOT / "templates" / "base" / "lib" / "app" / "pages" / "home_page.dart"
        bootstrap_template = REPO_ROOT / "templates" / "base" / "lib" / "bootstrap.dart"
        state_template = REPO_ROOT / "templates" / "base" / "lib" / "core" / "state_management" / "app_state.dart"

        self.assertIn("AppStateScope", app_template.read_text())
        self.assertIn("configureDependencies", bootstrap_template.read_text())
        self.assertIn("AppStateScope.of(context)", home_page_template.read_text())
        self.assertIn("class AppStateController", state_template.read_text())


if __name__ == "__main__":
    unittest.main()
