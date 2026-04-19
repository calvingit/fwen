"""Unit tests for the CLI module."""

import sys
import unittest
from pathlib import Path

# Add source directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fwen.cli import create_parser, parse_args, validate_args


class TestCli(unittest.TestCase):
    """Test cases for CLI helpers."""

    def test_parser_uses_fwen_program_name(self):
        """Help output should identify the published CLI name."""
        parser = create_parser()
        self.assertEqual(parser.prog, "fwen")

    def test_validate_args_rejects_invalid_project_name(self):
        """Project-name validation should work without legacy import paths."""
        args = parse_args(["--project-name", "InvalidName"])

        is_valid, error = validate_args(args)

        self.assertFalse(is_valid)
        self.assertIn("Invalid project name", error)


if __name__ == "__main__":
    unittest.main()
