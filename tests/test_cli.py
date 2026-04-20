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

    def test_parse_templates_list_command(self):
        """Templates command should parse command and action."""
        args = parse_args(["templates", "list"])

        self.assertEqual(args.command, "templates")
        self.assertEqual(args.template_action, "list")

    def test_parse_templates_explain_command_with_overrides(self):
        """Templates explain should accept architecture overrides."""
        args = parse_args(
            [
                "templates",
                "explain",
                "--state-management",
                "riverpod",
                "--navigation",
                "auto_route",
                "--no-examples",
            ]
        )

        self.assertEqual(args.command, "templates")
        self.assertEqual(args.template_action, "explain")
        self.assertEqual(args.state_management, "riverpod")
        self.assertEqual(args.navigation, "auto_route")
        self.assertTrue(args.no_examples)


if __name__ == "__main__":
    unittest.main()
