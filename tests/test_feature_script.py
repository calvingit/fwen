"""Integration tests for the feature generator script."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
FEATURE_SCRIPT = REPO_ROOT / "scripts" / "feature-dev.py"


class TestFeatureScript(unittest.TestCase):
    """Verify feature generation behavior using the real script."""

    def test_feature_name_preserves_pascal_case_and_snake_case(self):
        """PascalCase input should generate PascalCase class names and snake_case paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "lib").mkdir()

            result = subprocess.run(
                [sys.executable, str(FEATURE_SCRIPT), "DemoFeature"],
                cwd=project_root,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)

            entity_path = (
                project_root
                / "lib"
                / "features"
                / "demo_feature"
                / "domain"
                / "entities"
                / "demo_feature_entity.dart"
            )
            page_path = (
                project_root
                / "lib"
                / "features"
                / "demo_feature"
                / "presentation"
                / "pages"
                / "demo_feature_page.dart"
            )

            self.assertTrue(entity_path.exists())
            self.assertTrue(page_path.exists())
            self.assertIn("class DemoFeatureEntity", entity_path.read_text())
            self.assertIn("class DemoFeaturePage", page_path.read_text())


if __name__ == "__main__":
    unittest.main()
