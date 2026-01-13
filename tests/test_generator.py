"""
Unit tests for the Generator module.
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.config import Config
from modules.generator import ProjectGenerator, generate_project


class TestProjectGenerator(unittest.TestCase):
    """Test cases for ProjectGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.templates_dir = Path(self.test_dir) / "templates"
        self.output_dir = Path(self.test_dir) / "output"

        # Create template structure
        self.templates_dir.mkdir(parents=True)
        (self.templates_dir / "base" / "lib").mkdir(parents=True)
        (self.templates_dir / "base" / "lib" / "main.dart").write_text(
            "void main() => runApp({{ProjectName}}());"
        )
        (self.templates_dir / "state_management" / "bloc" / "lib").mkdir(parents=True)
        (self.templates_dir / "state_management" / "bloc" / "lib" / "bloc.dart").write_text(
            "class {{ProjectName}}Bloc {}"
        )

        self.output_dir.mkdir(parents=True)

        # Create config
        self.config = Config()
        self.config.set("project_name", "test_app")
        self.config.set("org_id", "com.example")
        self.config.set("state_management", "bloc")
        self.config.set("output_dir", str(self.output_dir))

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_initialization(self):
        """Test ProjectGenerator initialization."""
        generator = ProjectGenerator(self.config, self.templates_dir)

        self.assertEqual(generator.config, self.config)
        self.assertEqual(generator.templates_dir, self.templates_dir)
        self.assertIsNone(generator.project_path)

    @patch("modules.generator.run_command")
    def test_create_flutter_project_success(self, mock_run_command):
        """Test successful Flutter project creation."""
        mock_run_command.return_value = (True, "Flutter project created", "")

        generator = ProjectGenerator(self.config, self.templates_dir)
        success, message = generator._create_flutter_project()

        self.assertTrue(success)
        self.assertIn("created", message.lower())

    @patch("modules.generator.run_command")
    def test_create_flutter_project_failure(self, mock_run_command):
        """Test failed Flutter project creation."""
        mock_run_command.return_value = (False, "", "Error creating project")

        generator = ProjectGenerator(self.config, self.templates_dir)
        success, message = generator._create_flutter_project()

        self.assertFalse(success)
        self.assertIn("Error", message)

    @patch("modules.generator.run_command")
    def test_generate_calls_flutter_create(self, mock_run_command):
        """Test that generate() calls flutter create with correct arguments."""
        mock_run_command.return_value = (True, "Success", "")

        # Mock other methods to avoid actual file operations
        with patch.object(ProjectGenerator, "_apply_templates", return_value=(True, "")):
            with patch.object(ProjectGenerator, "_update_pubspec", return_value=(True, "")):
                generator = ProjectGenerator(self.config, self.templates_dir)
                success, message = generator.generate()

        # Verify flutter create was called
        mock_run_command.assert_called_once()
        args = mock_run_command.call_args[0][0]
        self.assertIn("flutter", args)
        self.assertIn("create", args)
        self.assertIn("--org", args)
        self.assertIn("com.example", args)

    @patch("modules.generator.copy_directory")
    @patch("modules.generator.run_command")
    def test_apply_templates_copies_base_templates(self, mock_run_command, mock_copy):
        """Test that base templates are copied."""
        mock_run_command.return_value = (True, "", "")
        mock_copy.return_value = None

        # Create a fake project directory
        project_dir = self.output_dir / "test_app"
        project_dir.mkdir(parents=True)
        (project_dir / "lib").mkdir()

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, message = generator._apply_templates()

        self.assertTrue(success)
        # Verify base templates were copied
        self.assertTrue(mock_copy.called)

    @patch("modules.generator.copy_directory")
    @patch("modules.generator.run_command")
    def test_apply_templates_copies_state_management(self, mock_run_command, mock_copy):
        """Test that state management templates are copied."""
        mock_run_command.return_value = (True, "", "")
        mock_copy.return_value = None

        # Create a fake project directory
        project_dir = self.output_dir / "test_app"
        project_dir.mkdir(parents=True)
        (project_dir / "lib").mkdir()

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, message = generator._apply_templates()

        self.assertTrue(success)

    @patch("modules.generator.merge_pubspec_dependencies")
    def test_update_pubspec_success(self, mock_merge):
        """Test successful pubspec update."""
        mock_merge.return_value = None

        # Create a fake project with pubspec.yaml
        project_dir = self.output_dir / "test_app"
        project_dir.mkdir(parents=True)
        (project_dir / "pubspec.yaml").write_text("name: test_app\n")

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, message = generator._update_pubspec()

        self.assertTrue(success)
        mock_merge.assert_called_once()

    @patch("modules.generator.merge_pubspec_dependencies")
    def test_update_pubspec_no_file(self, mock_merge):
        """Test pubspec update when file doesn't exist."""
        # Create project without pubspec.yaml
        project_dir = self.output_dir / "test_app"
        project_dir.mkdir(parents=True)

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, message = generator._update_pubspec()

        self.assertFalse(success)
        self.assertIn("not found", message)

    def test_get_project_path_before_generation(self):
        """Test getting project path before generation."""
        generator = ProjectGenerator(self.config, self.templates_dir)

        path = generator.get_project_path()
        self.assertEqual(path, Path())

    def test_get_project_path_after_generation(self):
        """Test getting project path after setting."""
        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = self.output_dir / "test_app"

        path = generator.get_project_path()
        self.assertEqual(path, self.output_dir / "test_app")


class TestGenerateProject(unittest.TestCase):
    """Test cases for generate_project module function."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.templates_dir = Path(self.test_dir) / "templates"
        self.output_dir = Path(self.test_dir) / "output"

        # Create minimal template structure
        self.templates_dir.mkdir(parents=True)
        (self.templates_dir / "base" / "lib").mkdir(parents=True)
        self.output_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    @patch("modules.generator.run_command")
    @patch("modules.generator.ProjectGenerator._apply_templates")
    @patch("modules.generator.ProjectGenerator._update_pubspec")
    def test_generate_project_success(self, mock_pubspec, mock_templates, mock_run):
        """Test successful project generation."""
        mock_run.return_value = (True, "", "")
        mock_templates.return_value = (True, "")
        mock_pubspec.return_value = (True, "")

        config = Config()
        config.set("project_name", "test_app")
        config.set("org_id", "com.example")
        config.set("output_dir", str(self.output_dir))

        success, message, path = generate_project(config, self.templates_dir)

        self.assertTrue(success)
        self.assertIsInstance(path, Path)

    @patch("modules.generator.run_command")
    def test_generate_project_flutter_failure(self, mock_run):
        """Test project generation when Flutter create fails."""
        mock_run.return_value = (False, "", "Flutter error")

        config = Config()
        config.set("project_name", "test_app")
        config.set("org_id", "com.example")
        config.set("output_dir", str(self.output_dir))

        success, message, path = generate_project(config, self.templates_dir)

        self.assertFalse(success)
        self.assertEqual(path, Path())


if __name__ == "__main__":
    unittest.main()
