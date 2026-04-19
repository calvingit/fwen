"""
Unit tests for the Utils module.
"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fwen.utils import (
    check_flutter_installed,
    copy_directory,
    copy_file_with_substitution,
    create_directory_structure,
    get_connected_devices,
    get_flutter_executable,
    merge_pubspec_dependencies,
    print_tree,
    run_command,
    validate_output_directory,
)


class TestRunCommand(unittest.TestCase):
    """Test cases for shell command execution."""

    @patch("fwen.utils.subprocess.run")
    def test_returns_success_tuple_from_subprocess(self, mock_run):
        """Successful subprocess execution should return stdout and stderr."""
        mock_run.return_value = Mock(returncode=0, stdout="ok", stderr="")

        success, stdout, stderr = run_command(["echo", "ok"])

        self.assertTrue(success)
        self.assertEqual(stdout, "ok")
        self.assertEqual(stderr, "")

    @patch("fwen.utils.subprocess.run", side_effect=OSError("boom"))
    def test_returns_failure_tuple_when_subprocess_raises(self, mock_run):
        """Execution errors should be converted into a failure tuple."""
        success, stdout, stderr = run_command(["missing-command"])

        self.assertFalse(success)
        self.assertEqual(stdout, "")
        self.assertIn("boom", stderr)


class TestGetFlutterExecutable(unittest.TestCase):
    """Test cases for Flutter executable detection."""

    def test_returns_string(self):
        """Test that get_flutter_executable returns a string."""
        result = get_flutter_executable()
        self.assertIsInstance(result, str)

    def test_flutter_env_var(self):
        """Test that FLUTTER_ROOT environment variable is respected."""
        # Save original value
        original = os.environ.get("FLUTTER_ROOT")

        # Test with custom FLUTTER_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["FLUTTER_ROOT"] = tmpdir
            result = get_flutter_executable()
            self.assertIn("flutter", result.lower())

        # Restore original value
        if original is not None:
            os.environ["FLUTTER_ROOT"] = original
        elif "FLUTTER_ROOT" in os.environ:
            del os.environ["FLUTTER_ROOT"]


class TestCopyFileWithSubstitution(unittest.TestCase):
    """Test cases for copy_file_with_substitution function."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.src_file = Path(self.test_dir) / "source.txt"
        self.dest_file = Path(self.test_dir) / "dest.txt"

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_creates_dest_file(self):
        """Test that destination file is created."""
        self.src_file.write_text("test content")

        copy_file_with_substitution(self.src_file, self.dest_file, {})

        self.assertTrue(self.dest_file.exists())

    def test_creates_parent_directories(self):
        """Test that parent directories are created."""
        self.src_file.write_text("test")
        dest_with_parents = self.dest_file / "subdir" / "file.txt"

        copy_file_with_substitution(self.src_file, dest_with_parents, {})

        self.assertTrue(dest_with_parents.exists())

    def test_performs_substitutions(self):
        """Test that variable substitutions are performed."""
        content = "Hello {{name}}, welcome to {{app}}!"
        self.src_file.write_text(content)

        substitutions = {
            "name": "World",
            "app": "MyApp",
        }

        copy_file_with_substitution(self.src_file, self.dest_file, substitutions)

        result = self.dest_file.read_text()
        self.assertEqual(result, "Hello World, welcome to MyApp!")

    def test_partial_substitutions(self):
        """Test that only existing variables are substituted."""
        content = "Hello {{name}}, {{undefined}}!"
        self.src_file.write_text(content)

        substitutions = {"name": "World"}

        copy_file_with_substitution(self.src_file, self.dest_file, substitutions)

        result = self.dest_file.read_text()
        self.assertEqual(result, "Hello World, {{undefined}}!")


class TestCopyDirectory(unittest.TestCase):
    """Test cases for copy_directory function."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.src_dir = Path(self.test_dir) / "source"
        self.dest_dir = Path(self.test_dir) / "dest"

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_copies_files(self):
        """Test that files are copied."""
        (self.src_dir / "file.txt").parent.mkdir(parents=True)
        (self.src_dir / "file.txt").write_text("content {{var}}")

        copy_directory(self.src_dir, self.dest_dir, {"var": "value"})

        self.assertTrue((self.dest_dir / "file.txt").exists())

    def test_applies_substitutions(self):
        """Test that substitutions are applied to all files."""
        (self.src_dir / "subdir").mkdir(parents=True)
        (self.src_dir / "file1.txt").write_text("{{var1}}")
        (self.src_dir / "subdir" / "file2.txt").write_text("{{var2}}")

        copy_directory(self.src_dir, self.dest_dir, {"var1": "A", "var2": "B"})

        self.assertEqual((self.dest_dir / "file1.txt").read_text(), "A")
        self.assertEqual((self.dest_dir / "subdir" / "file2.txt").read_text(), "B")

    def test_respects_ignore_patterns(self):
        """Test that ignore patterns are respected for files."""
        (self.src_dir / "test.txt").parent.mkdir(parents=True)
        (self.src_dir / "test.txt").write_text("test")
        (self.src_dir / "test.pyc").write_text("compiled")
        (self.src_dir / "test.pyo").write_text("optimized")

        copy_directory(
            self.src_dir,
            self.dest_dir,
            {},
            ignore_patterns=["*.pyc", "*.pyo"],
        )

        self.assertTrue((self.dest_dir / "test.txt").exists())
        self.assertFalse((self.dest_dir / "test.pyc").exists())
        self.assertFalse((self.dest_dir / "test.pyo").exists())

    def test_ignores_directories_when_copying(self):
        """Directory entries returned by rglob should be skipped."""
        (self.src_dir / "subdir").mkdir(parents=True)

        copy_directory(self.src_dir, self.dest_dir, {})

        self.assertFalse((self.dest_dir / "subdir").exists())


class TestMergePubspecDependencies(unittest.TestCase):
    """Test cases for pubspec dependency merging."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.pubspec_path = Path(self.test_dir) / "pubspec.yaml"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_merges_missing_dependency_sections(self):
        """Missing dependency sections should be created before merging."""
        self.pubspec_path.write_text("name: demo_app\n")

        merge_pubspec_dependencies(
            self.pubspec_path,
            {"dio": "^5.4.0"},
            {"build_runner": "^2.4.0"},
        )

        content = self.pubspec_path.read_text()
        self.assertIn("dependencies:", content)
        self.assertIn("dio: ^5.4.0", content)
        self.assertIn("dev_dependencies:", content)
        self.assertIn("build_runner: ^2.4.0", content)


class TestCheckFlutterInstalled(unittest.TestCase):
    """Test cases for Flutter installation detection."""

    @patch("fwen.utils.run_command", return_value=(True, "Flutter 3.0", ""))
    def test_returns_success_output(self, mock_run_command):
        """Successful version checks should return stdout."""
        success, message = check_flutter_installed()

        self.assertTrue(success)
        self.assertEqual(message, "Flutter 3.0")

    @patch("fwen.utils.run_command", return_value=(False, "", "not found"))
    def test_returns_stderr_when_flutter_missing(self, mock_run_command):
        """Failed version checks should return stderr."""
        success, message = check_flutter_installed()

        self.assertFalse(success)
        self.assertEqual(message, "not found")

    @patch("fwen.utils.run_command", return_value=(False, "", ""))
    def test_returns_default_message_when_no_stderr(self, mock_run_command):
        """Failed version checks without stderr should use a default message."""
        success, message = check_flutter_installed()

        self.assertFalse(success)
        self.assertEqual(message, "Flutter not found in PATH")


class TestGetConnectedDevices(unittest.TestCase):
    """Test cases for parsing flutter devices output."""

    @patch("fwen.utils.run_command", return_value=(False, "", ""))
    def test_returns_empty_list_when_command_fails(self, mock_run_command):
        """Device enumeration failures should return an empty list."""
        self.assertEqual(get_connected_devices(), [])

    @patch(
        "fwen.utils.run_command",
        return_value=(
            True,
            "\n".join(
                [
                    "2 connected devices:",
                    "iPhone 16 • ios-sim • ios",
                    "Pixel 9 • android-emulator • android",
                    "Malformed line",
                    "",
                ]
            ),
            "",
        ),
    )
    def test_parses_connected_devices_output(self, mock_run_command):
        """Well-formed device lines should be converted into dictionaries."""
        devices = get_connected_devices()

        self.assertEqual(
            devices,
            [
                {"id": "ios-sim", "name": "ios"},
                {"id": "android-emulator", "name": "android"},
            ],
        )


class TestCreateDirectoryStructure(unittest.TestCase):
    """Test cases for directory-structure creation."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_creates_declared_directories_and_files(self):
        """Nested directories and files should be created from the structure map."""
        create_directory_structure(
            Path(self.test_dir),
            {
                "lib": ["main.dart", "features"],
                "lib/features": ["auth"],
            },
        )

        self.assertTrue((Path(self.test_dir) / "lib" / "main.dart").exists())
        self.assertTrue((Path(self.test_dir) / "lib" / "features").is_dir())
        self.assertTrue((Path(self.test_dir) / "lib" / "features" / "auth").is_dir())


class TestValidateOutputDirectory(unittest.TestCase):
    """Test cases for validate_output_directory function."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_nonexistent_directory(self):
        """Test validation of nonexistent directory."""
        path = Path(self.test_dir) / "new_dir"
        is_valid, error = validate_output_directory(path)

        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_existing_empty_directory(self):
        """Test validation of existing empty directory."""
        empty_dir = Path(self.test_dir) / "empty"
        empty_dir.mkdir()

        is_valid, error = validate_output_directory(empty_dir)

        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_existing_file(self):
        """Test validation when path is a file, not directory."""
        file_path = Path(self.test_dir) / "file.txt"
        file_path.write_text("content")

        is_valid, error = validate_output_directory(file_path)

        self.assertFalse(is_valid)
        self.assertIn("not a directory", error)

    def test_existing_nonempty_directory(self):
        """Test validation of existing non-empty directory."""
        nonempty_dir = Path(self.test_dir) / "nonempty"
        nonempty_dir.mkdir()
        (nonempty_dir / "file.txt").write_text("content")

        is_valid, error = validate_output_directory(nonempty_dir)

        self.assertFalse(is_valid)
        self.assertIn("not empty", error)


class TestPrintTree(unittest.TestCase):
    """Test cases for print_tree function."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_prints_directory_structure(self):
        """Test that directory structure is printed."""
        # Create test structure
        (Path(self.test_dir) / "dir1").mkdir()
        (Path(self.test_dir) / "dir2").mkdir()
        (Path(self.test_dir) / "file.txt").write_text("content")

        # Just verify it doesn't crash (output is to stdout)
        try:
            print_tree(Path(self.test_dir), max_depth=2)
        except Exception as e:
            self.fail(f"print_tree raised an exception: {e}")

    def test_respects_max_depth(self):
        """Test that max_depth is respected."""
        # Create nested structure
        (Path(self.test_dir) / "dir1" / "dir2" / "dir3").mkdir(parents=True)

        # Should not crash with max_depth=1
        try:
            print_tree(Path(self.test_dir), max_depth=1)
        except Exception as e:
            self.fail(f"print_tree raised an exception: {e}")

    def test_handles_nonexistent_directory(self):
        """Test handling of nonexistent directory."""
        # Should not crash
        try:
            print_tree(Path(self.test_dir) / "nonexistent")
        except Exception:
            # Expected to handle gracefully
            pass

    def test_handles_permission_error(self):
        """Permission errors should be swallowed when listing a directory."""
        with patch("pathlib.Path.iterdir", side_effect=PermissionError):
            print_tree(Path(self.test_dir))


if __name__ == "__main__":
    unittest.main()
