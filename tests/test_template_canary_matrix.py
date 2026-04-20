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

                            self.assertTrue((project_dir / "lib" / "main.dart").exists())
                            self.assertTrue((project_dir / "lib" / "bootstrap.dart").exists())
                            self.assertTrue(app_file.exists())
                            self.assertTrue(state_file.exists())
                            self.assertTrue(router_file.exists())

                            app_content = app_file.read_text()
                            self.assertIn("MatrixCanaryApp", app_content)
                            self.assertNotIn("{{ProjectName}}", app_content)

                            state_content = state_file.read_text()
                            self.assertIn(STATE_KEYWORDS[state_management], state_content)
                            self.assertNotIn("{{ProjectName}}", state_content)

                            router_content = router_file.read_text()
                            self.assertIn(NAVIGATION_KEYWORDS[navigation], router_content)
                            self.assertNotIn("{{ProjectName}}", router_content)

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


if __name__ == "__main__":
    unittest.main()
