"""Canary matrix tests for template combinations."""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fwen.config import Config
from fwen.generator import ProjectGenerator

REPO_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates"

STATE_KEYWORDS = {
    "bloc": "AppBlocManager",
    "provider": "AppProviderManager",
    "riverpod": "ProviderContainer",
}

NAVIGATION_KEYWORDS = {
    "go_router": "GoRouter",
    "auto_route": "RootStackRouter",
    "navigator": "onGenerateRoute",
}


class TestTemplateCanaryMatrix(unittest.TestCase):
    """Verify core template combinations remain generation-safe."""

    def _build_config(
        self, output_dir: Path, state_management: str, navigation: str, include_examples: bool
    ) -> Config:
        """Build a config for matrix canary checks."""
        config = Config()
        config.update(
            {
                "project_name": "matrix_canary_app",
                "org_id": "com.example",
                "output_dir": str(output_dir),
                "state_management": state_management,
                "navigation": navigation,
                "include_examples": include_examples,
            }
        )
        return config

    def test_matrix_state_navigation_examples(self):
        """Run canary checks on 3x3x2 state/nav/examples combinations."""
        for state_management in Config.STATE_MANAGEMENT_OPTIONS:
            for navigation in Config.NAVIGATION_OPTIONS:
                for include_examples in [False, True]:
                    with self.subTest(
                        state_management=state_management,
                        navigation=navigation,
                        include_examples=include_examples,
                    ):
                        temp_dir = Path(tempfile.mkdtemp())
                        try:
                            project_dir = temp_dir / "matrix_canary_app"
                            (project_dir / "lib").mkdir(parents=True, exist_ok=True)

                            config = self._build_config(
                                output_dir=temp_dir,
                                state_management=state_management,
                                navigation=navigation,
                                include_examples=include_examples,
                            )
                            generator = ProjectGenerator(config, TEMPLATES_DIR)
                            generator.project_path = project_dir

                            success, message = generator._apply_templates()
                            self.assertTrue(success, message)

                            app_file = project_dir / "lib" / "app" / "app.dart"
                            state_file = (
                                project_dir
                                / "lib"
                                / "core"
                                / "state_management"
                                / "app_state_management.dart"
                            )
                            router_file = project_dir / "lib" / "app" / "router" / "app_router.dart"
                            foundation_file = (
                                project_dir / "lib" / "core" / "constants" / "app_constants.dart"
                            )
                            failures_file = (
                                project_dir / "lib" / "core" / "errors" / "failures.dart"
                            )
                            logger_file = project_dir / "lib" / "core" / "utils" / "logger.dart"

                            self.assertTrue((project_dir / "lib" / "main.dart").exists())
                            self.assertTrue((project_dir / "lib" / "bootstrap.dart").exists())
                            self.assertTrue(app_file.exists())
                            self.assertTrue(state_file.exists())
                            self.assertTrue(router_file.exists())
                            self.assertTrue(foundation_file.exists())
                            self.assertTrue(failures_file.exists())
                            self.assertTrue(logger_file.exists())

                            app_content = app_file.read_text()
                            self.assertIn("MatrixCanaryApp", app_content)
                            self.assertNotIn("{{ProjectName}}", app_content)

                            state_content = state_file.read_text()
                            self.assertIn(STATE_KEYWORDS[state_management], state_content)
                            self.assertNotIn("{{ProjectName}}", state_content)

                            router_content = router_file.read_text()
                            self.assertIn(NAVIGATION_KEYWORDS[navigation], router_content)
                            self.assertNotIn("{{ProjectName}}", router_content)

                            foundation_content = foundation_file.read_text()
                            self.assertIn("class AppConstants", foundation_content)
                            self.assertNotIn("{{ProjectName}}", foundation_content)

                            scenario_auth_file = (
                                project_dir
                                / "lib"
                                / "features"
                                / "auth"
                                / "domain"
                                / "usecases"
                                / "get_signed_in_user_usecase.dart"
                            )
                            if include_examples:
                                self.assertTrue(scenario_auth_file.exists())
                                scenario_auth_content = scenario_auth_file.read_text()
                                self.assertIn("matrix_canary_app-auth-user", scenario_auth_content)
                                self.assertNotIn("{{project_name}}", scenario_auth_content)
                            else:
                                self.assertFalse(scenario_auth_file.exists())
                        finally:
                            shutil.rmtree(temp_dir)


class TestExtensionTemplatesExist(unittest.TestCase):
    """Verify implemented extension templates have all required files on disk."""

    def test_auth_template_files_exist(self):
        expected_files = [
            "lib/features/auth/domain/entities/auth_user.dart",
            "lib/features/auth/domain/repositories/auth_repository.dart",
            "lib/features/auth/domain/usecases/sign_in_with_email_usecase.dart",
            "lib/features/auth/domain/usecases/sign_out_usecase.dart",
            "lib/features/auth/data/datasources/auth_remote_datasource.dart",
            "lib/features/auth/data/repositories/auth_repository_impl.dart",
            "lib/features/auth/presentation/manager/auth_manager.dart",
            "lib/features/auth/presentation/pages/login_page.dart",
        ]
        auth_dir = TEMPLATES_DIR / "auth"
        for rel_path in expected_files:
            with self.subTest(file=rel_path):
                self.assertTrue((auth_dir / rel_path).exists(), f"Missing: {rel_path}")

    def test_persistence_template_files_exist(self):
        expected_files = [
            "lib/core/storage/storage_service.dart",
            "lib/core/storage/shared_preferences_storage.dart",
        ]
        persist_dir = TEMPLATES_DIR / "persistence"
        for rel_path in expected_files:
            with self.subTest(file=rel_path):
                self.assertTrue((persist_dir / rel_path).exists(), f"Missing: {rel_path}")

    def test_analytics_template_files_exist(self):
        expected_files = [
            "lib/core/analytics/analytics_service.dart",
            "lib/core/analytics/firebase_analytics_service.dart",
            "lib/core/analytics/sentry_analytics_service.dart",
            "lib/core/analytics/mixpanel_analytics_service.dart",
        ]
        analytics_dir = TEMPLATES_DIR / "analytics"
        for rel_path in expected_files:
            with self.subTest(file=rel_path):
                self.assertTrue((analytics_dir / rel_path).exists(), f"Missing: {rel_path}")

    def test_firebase_service_template_files_exist(self):
        service_files = {
            "auth": "lib/core/firebase/firebase_auth_service.dart",
            "firestore": "lib/core/firebase/firestore_service.dart",
            "functions": "lib/core/firebase/functions_service.dart",
            "analytics": "lib/core/firebase/firebase_analytics_service.dart",
            "messaging": "lib/core/firebase/messaging_service.dart",
            "storage": "lib/core/firebase/storage_service.dart",
            "remote_config": "lib/core/firebase/remote_config_service.dart",
            "crashlytics": "lib/core/firebase/crashlytics_service.dart",
        }
        for service, rel_path in service_files.items():
            with self.subTest(service=service):
                self.assertTrue(
                    (TEMPLATES_DIR / "firebase" / service / rel_path).exists(),
                    f"Missing firebase/{service}/{rel_path}",
                )

    def test_auth_template_variables_not_substituted(self):
        """Template source files must still contain raw {{...}} placeholders."""
        datasource = (
            TEMPLATES_DIR
            / "auth/lib/features/auth/data/datasources/auth_remote_datasource.dart"
        )
        content = datasource.read_text()
        self.assertIn("{{project_name}}", content)

    def test_extension_templates_applied_when_selected(self):
        """Generator copies auth/persistence/analytics templates for matching config."""
        import shutil
        import tempfile
        from unittest.mock import patch

        temp_dir = Path(tempfile.mkdtemp())
        try:
            project_dir = temp_dir / "ext_test_app"
            (project_dir / "lib").mkdir(parents=True, exist_ok=True)

            config = Config()
            config.update(
                {
                    "project_name": "ext_test_app",
                    "org_id": "com.example",
                    "output_dir": str(temp_dir),
                    "include_auth": True,
                    "include_persistence": True,
                    "include_analytics": True,
                    "analytics_choice": "sentry",
                    "include_examples": False,
                }
            )

            from fwen.generator import ProjectGenerator

            generator = ProjectGenerator(config, TEMPLATES_DIR)
            generator.project_path = project_dir
            success, message = generator._apply_templates()

            self.assertTrue(success, message)

            login_page = project_dir / "lib/features/auth/presentation/pages/login_page.dart"
            self.assertTrue(login_page.exists(), "auth login_page not generated")
            self.assertNotIn("{{ProjectName}}", login_page.read_text())

            storage = project_dir / "lib/core/storage/storage_service.dart"
            self.assertTrue(storage.exists(), "persistence storage_service not generated")

            analytics = project_dir / "lib/core/analytics/analytics_service.dart"
            self.assertTrue(analytics.exists(), "analytics_service not generated")
        finally:
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    unittest.main()
