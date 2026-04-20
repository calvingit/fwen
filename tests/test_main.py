"""Unit tests for the CLI entrypoint module."""

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

# Add source directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import fwen.__main__ as main_module
from fwen.config import Config


class TestMainHelpers(unittest.IsolatedAsyncioTestCase):
    """Tests for helper functions in __main__.py."""

    def test_print_banner_skips_when_disabled(self):
        """The banner helper should not print anything when disabled."""
        console = Mock()

        main_module.print_banner(console, show_banner=False)

        console.print.assert_not_called()

    def test_print_banner_renders_when_enabled(self):
        """The banner helper should render the banner in interactive mode."""
        console = Mock()

        main_module.print_banner(console, show_banner=True)

        console.print.assert_called_once()

    def test_print_error_formats_message(self):
        """Error messages should render with the red error style."""
        console = Mock()

        main_module.print_error(console, "boom")

        console.print.assert_called_once_with("\n[red]✗ Error: boom[/red]\n")

    def test_print_info_formats_message(self):
        """Info messages should render with the blue info style."""
        console = Mock()

        main_module.print_info(console, "details")

        console.print.assert_called_once_with("\n[blue]ℹ details[/blue]\n")

    def test_print_success_formats_message(self):
        """Success messages should render with the green success style."""
        console = Mock()

        main_module.print_success(console, "done")

        console.print.assert_called_once_with("\n[green]✓ done[/green]\n")

    def test_print_config_summary_includes_optional_rows(self):
        """Config summaries should print tables including optional firebase and feature rows."""
        console = Mock()

        main_module.print_config_summary(
            console,
            {
                "project_name": "demo",
                "org_id": "com.example",
                "state_management": "bloc",
                "navigation": "go_router",
                "platforms": ["ios", "android"],
                "include_firebase": True,
                "firebase_services": ["auth"],
                "create_feature": True,
                "feature_name": "Auth",
            },
        )

        console.print.assert_called_once()

    def test_is_template_command_detects_templates_mode(self):
        """Template command mode should be detected from parsed args."""
        self.assertTrue(main_module.is_template_command(SimpleNamespace(command="templates")))
        self.assertFalse(main_module.is_template_command(SimpleNamespace(command=None)))

    def test_run_template_command_list_renders_registry(self):
        """Template list command should print a registry table."""
        console = Mock()
        args = SimpleNamespace(template_action="list")

        main_module.run_template_command(args, console)

        self.assertTrue(console.print.called)

    def test_run_template_command_explain_renders_selection(self):
        """Template explain command should print config and selection details."""
        console = Mock()
        args = SimpleNamespace(template_action="explain")

        with patch.object(
            main_module,
            "args_to_config",
            return_value={
                "state_management": "riverpod",
                "navigation": "auto_route",
                "include_examples": False,
                "include_testing": False,
            },
        ):
            main_module.run_template_command(args, console)

        self.assertTrue(console.print.called)

    async def test_run_non_interactive_mode_success(self):
        """The non-interactive path should update config and print next steps."""
        args = SimpleNamespace(yes=True)
        console = Mock()
        config = Config()

        with (
            patch.object(main_module, "args_to_config", return_value={"project_name": "demo_app"}),
            patch.object(
                main_module,
                "generate_project",
                return_value=(True, "Created", Path("/tmp/demo_app")),
            ),
            patch.object(main_module, "print_config_summary"),
            patch.object(main_module, "print_success"),
        ):
            await main_module.run_non_interactive_mode(
                args, console, config, Path("/tmp/templates")
            )

        self.assertEqual(config.get("project_name"), "demo_app")
        console.print.assert_any_call("\n[bold]Next steps:[/bold]")
        console.print.assert_any_call("  cd /tmp/demo_app")

    async def test_run_non_interactive_mode_failure_exits(self):
        """The non-interactive path should exit when generation fails."""
        args = SimpleNamespace(yes=True)
        console = Mock()
        config = Config()

        with (
            patch.object(main_module, "args_to_config", return_value={"project_name": "demo_app"}),
            patch.object(main_module, "generate_project", return_value=(False, "boom", None)),
            patch.object(main_module, "print_config_summary"),
            patch.object(main_module, "print_error"),
        ):
            with self.assertRaises(SystemExit) as exc_info:
                await main_module.run_non_interactive_mode(
                    args, console, config, Path("/tmp/templates")
                )

        self.assertEqual(exc_info.exception.code, 1)

    async def test_run_non_interactive_mode_rejects_confirmation(self):
        """Entering a non-yes response should cancel before generation starts."""
        args = SimpleNamespace(yes=False)
        console = Mock()
        config = Config()

        with (
            patch.object(main_module, "args_to_config", return_value={"project_name": "demo_app"}),
            patch.object(main_module, "generate_project") as mock_generate_project,
            patch.object(main_module, "print_config_summary"),
            patch("builtins.input", return_value="n"),
        ):
            with self.assertRaises(SystemExit) as exc_info:
                await main_module.run_non_interactive_mode(
                    args, console, config, Path("/tmp/templates")
                )

        self.assertEqual(exc_info.exception.code, 0)
        mock_generate_project.assert_not_called()

    async def test_run_non_interactive_mode_handles_keyboard_interrupt_during_confirmation(self):
        """Interrupting the confirmation prompt should cancel cleanly."""
        args = SimpleNamespace(yes=False)
        console = Mock()
        config = Config()

        with (
            patch.object(main_module, "args_to_config", return_value={"project_name": "demo_app"}),
            patch.object(main_module, "generate_project") as mock_generate_project,
            patch.object(main_module, "print_config_summary"),
            patch("builtins.input", side_effect=KeyboardInterrupt),
        ):
            with self.assertRaises(SystemExit) as exc_info:
                await main_module.run_non_interactive_mode(
                    args, console, config, Path("/tmp/templates")
                )

        self.assertEqual(exc_info.exception.code, 0)
        mock_generate_project.assert_not_called()

    async def test_run_interactive_mode_cancel_exits(self):
        """The interactive path should exit cleanly when the summary is rejected."""
        console = Mock()
        config = Config()
        prompts_instance = Mock()
        prompts_instance.confirm_summary = AsyncMock(return_value=False)

        with (
            patch.object(
                main_module, "collect_user_config", AsyncMock(return_value={"project_name": "demo"})
            ),
            patch.object(main_module, "Prompts", return_value=prompts_instance),
        ):
            with self.assertRaises(SystemExit) as exc_info:
                await main_module.run_interactive_mode(console, config, Path("/tmp/templates"))

        self.assertEqual(exc_info.exception.code, 0)

    async def test_run_interactive_mode_failure_exits(self):
        """Interactive generation failures should exit with an error."""
        console = Mock()
        config = Config()
        prompts_instance = Mock()
        prompts_instance.confirm_summary = AsyncMock(return_value=True)

        with (
            patch.object(
                main_module, "collect_user_config", AsyncMock(return_value={"project_name": "demo"})
            ),
            patch.object(main_module, "Prompts", return_value=prompts_instance),
            patch.object(main_module, "generate_project", return_value=(False, "boom", None)),
            patch.object(main_module, "print_error"),
        ):
            with self.assertRaises(SystemExit) as exc_info:
                await main_module.run_interactive_mode(console, config, Path("/tmp/templates"))

        self.assertEqual(exc_info.exception.code, 1)


class TestMainEntrypoint(unittest.IsolatedAsyncioTestCase):
    """Tests for the main() coroutine."""

    async def test_main_exits_when_flutter_missing(self):
        """The CLI should stop early if Flutter is not installed."""
        console = Mock()

        with (
            patch.object(main_module, "parse_args", return_value=SimpleNamespace()),
            patch.object(main_module, "Console", return_value=console),
            patch.object(main_module, "check_flutter_installed", return_value=(False, "missing")),
            patch.object(main_module, "print_error"),
            patch.object(main_module, "print_info"),
        ):
            with self.assertRaises(SystemExit) as exc_info:
                await main_module.main()

        self.assertEqual(exc_info.exception.code, 1)

    async def test_main_exits_when_templates_missing(self):
        """The CLI should stop when the templates directory is missing."""
        console = Mock()

        with (
            patch.object(main_module, "parse_args", return_value=SimpleNamespace()),
            patch.object(main_module, "Console", return_value=console),
            patch.object(main_module, "check_flutter_installed", return_value=(True, "ok")),
            patch.object(
                main_module.Path,
                "exists",
                autospec=True,
                side_effect=lambda path_obj: not str(path_obj).endswith("/templates"),
            ),
            patch.object(main_module, "print_error"),
            patch.object(main_module, "print_info"),
        ):
            with self.assertRaises(SystemExit) as exc_info:
                await main_module.main()

        self.assertEqual(exc_info.exception.code, 1)

    async def test_main_rejects_invalid_args(self):
        """Invalid non-interactive arguments should exit before generation starts."""
        console = Mock()
        args = SimpleNamespace()

        with (
            patch.object(main_module, "parse_args", return_value=args),
            patch.object(main_module, "Console", return_value=console),
            patch.object(main_module, "check_flutter_installed", return_value=(True, "ok")),
            patch.object(main_module, "should_use_interactive_mode", return_value=False),
            patch.object(main_module, "validate_args", return_value=(False, "bad args")),
            patch.object(main_module, "print_error"),
        ):
            with self.assertRaises(SystemExit) as exc_info:
                await main_module.main()

        self.assertEqual(exc_info.exception.code, 1)

    async def test_main_runs_interactive_mode(self):
        """Interactive mode should delegate to the interactive runner."""
        console = Mock()
        args = SimpleNamespace()
        run_interactive_mode = AsyncMock()

        with (
            patch.object(main_module, "parse_args", return_value=args),
            patch.object(main_module, "Console", return_value=console),
            patch.object(main_module, "check_flutter_installed", return_value=(True, "ok")),
            patch.object(main_module, "should_use_interactive_mode", return_value=True),
            patch.object(main_module, "run_interactive_mode", run_interactive_mode),
            patch.object(main_module, "print_banner"),
        ):
            await main_module.main()

        run_interactive_mode.assert_awaited_once()

    async def test_main_runs_non_interactive_mode(self):
        """Non-interactive mode should validate arguments then run the non-interactive path."""
        console = Mock()
        args = SimpleNamespace()
        run_non_interactive_mode = AsyncMock()

        with (
            patch.object(main_module, "parse_args", return_value=args),
            patch.object(main_module, "Console", return_value=console),
            patch.object(main_module, "check_flutter_installed", return_value=(True, "ok")),
            patch.object(main_module, "should_use_interactive_mode", side_effect=[False, False]),
            patch.object(main_module, "validate_args", return_value=(True, None)),
            patch.object(main_module, "run_non_interactive_mode", run_non_interactive_mode),
            patch.object(main_module, "print_banner"),
        ):
            await main_module.main()

        run_non_interactive_mode.assert_awaited_once()

    async def test_main_handles_keyboard_interrupt(self):
        """KeyboardInterrupt from a runner should be converted into a clean exit."""
        console = Mock()
        args = SimpleNamespace()

        with (
            patch.object(main_module, "parse_args", return_value=args),
            patch.object(main_module, "Console", return_value=console),
            patch.object(main_module, "check_flutter_installed", return_value=(True, "ok")),
            patch.object(main_module, "should_use_interactive_mode", return_value=True),
            patch.object(
                main_module, "run_interactive_mode", AsyncMock(side_effect=KeyboardInterrupt)
            ),
            patch.object(main_module, "print_banner"),
        ):
            with self.assertRaises(SystemExit) as exc_info:
                await main_module.main()

        self.assertEqual(exc_info.exception.code, 0)

    async def test_main_handles_unexpected_exception(self):
        """Unexpected exceptions should be printed and exit with status 1."""
        console = Mock()
        args = SimpleNamespace()

        with (
            patch.object(main_module, "parse_args", return_value=args),
            patch.object(main_module, "Console", return_value=console),
            patch.object(main_module, "check_flutter_installed", return_value=(True, "ok")),
            patch.object(main_module, "should_use_interactive_mode", return_value=True),
            patch.object(
                main_module, "run_interactive_mode", AsyncMock(side_effect=RuntimeError("boom"))
            ),
            patch.object(main_module, "print_banner"),
            patch.object(main_module, "print_error"),
        ):
            with self.assertRaises(SystemExit) as exc_info:
                await main_module.main()

        self.assertEqual(exc_info.exception.code, 1)

    async def test_main_runs_template_command_without_flutter_check(self):
        """Template commands should execute without requiring Flutter installation."""
        console = Mock()
        args = SimpleNamespace(command="templates", template_action="list")
        run_template_command = Mock()

        with (
            patch.object(main_module, "parse_args", return_value=args),
            patch.object(main_module, "Console", return_value=console),
            patch.object(main_module, "run_template_command", run_template_command),
            patch.object(main_module, "check_flutter_installed") as mock_flutter,
        ):
            await main_module.main()

        run_template_command.assert_called_once_with(args, console)
        mock_flutter.assert_not_called()


if __name__ == "__main__":
    unittest.main()
