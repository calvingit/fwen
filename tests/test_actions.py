"""Unit tests for post-creation actions."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

# Add source directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fwen.actions import PostCreationActions, run_post_creation_actions


class PromptStub:
    """Simple async prompt stub for questionary helpers."""

    def __init__(self, value):
        self.value = value

    async def ask_async(self):
        return self.value


class DummyStatus:
    """Minimal context manager used to stub Console.status()."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class TestPostCreationActions(unittest.IsolatedAsyncioTestCase):
    """Test cases for PostCreationActions."""

    def setUp(self):
        self.project_path = Path("/tmp/example_project")
        self.actions = PostCreationActions(
            self.project_path,
            {
                "project_name": "demo_app",
                "state_management": "bloc",
                "navigation": "go_router",
                "platforms": ["ios", "android"],
                "include_firebase": True,
                "firebase_services": ["auth", "firestore"],
            },
        )
        self.actions.console = Mock()
        self.actions.console.status.return_value = DummyStatus()

    def test_feature_script_path_points_to_repo_script(self):
        """Feature creation should resolve the script from the current repository."""
        expected = Path(__file__).parent.parent / "scripts" / "feature-dev.py"
        self.assertEqual(self.actions._get_feature_script_path(), expected)

    def test_show_success_message_renders_panel(self):
        """Success rendering should print a summary panel."""
        self.actions.show_success_message()
        self.actions.console.print.assert_called_once()

    @patch("fwen.actions.questionary.select")
    async def test_run_action_menu_executes_until_exit(self, mock_select):
        """The action menu should keep looping until exit is selected."""
        mock_select.side_effect = [PromptStub("pub_get"), PromptStub("exit")]
        self.actions._execute_action = AsyncMock()

        await self.actions.run_action_menu()

        self.actions._execute_action.assert_awaited_once_with("pub_get")

    async def test_execute_action_runs_handler(self):
        """Known actions should dispatch to their coroutine handler."""
        self.actions._flutter_pub_get = AsyncMock()

        await self.actions._execute_action("pub_get")

        self.actions._flutter_pub_get.assert_awaited_once()

    async def test_execute_action_reports_handler_exception(self):
        """Handler exceptions should be printed instead of escaping."""
        self.actions._flutter_pub_get = AsyncMock(side_effect=RuntimeError("boom"))

        await self.actions._execute_action("pub_get")

        self.actions.console.print.assert_called_once_with("[red]Error: boom[/red]")

    @patch("fwen.actions.run_command", return_value=(True, "", ""))
    async def test_flutter_pub_get_success(self, mock_run_command):
        """flutter pub get success should print a success message."""
        await self.actions._flutter_pub_get()

        self.actions.console.print.assert_called_with("[green]✓ Dependencies installed[/green]")
        mock_run_command.assert_called_once()

    @patch("fwen.actions.run_command", return_value=(False, "", "pub get failed"))
    async def test_flutter_pub_get_failure(self, mock_run_command):
        """flutter pub get failure should print stderr."""
        await self.actions._flutter_pub_get()

        self.actions.console.print.assert_called_with(
            "[red]✗ Failed to install dependencies: pub get failed[/red]"
        )
        mock_run_command.assert_called_once()

    @patch("fwen.actions.run_command", return_value=(True, "", ""))
    async def test_run_build_runner_success(self, mock_run_command):
        """build_runner success should print a completion message."""
        await self.actions._run_build_runner()

        self.actions.console.print.assert_any_call("[green]✓ Code generation complete[/green]")
        mock_run_command.assert_called_once()

    @patch("fwen.actions.run_command", return_value=(False, "", "build failed"))
    async def test_run_build_runner_failure(self, mock_run_command):
        """build_runner failure should print stderr."""
        await self.actions._run_build_runner()

        self.actions.console.print.assert_any_call("[red]✗ Build failed: build failed[/red]")
        mock_run_command.assert_called_once()

    @patch("fwen.actions.run_command", return_value=(True, "", ""))
    async def test_open_vscode_success(self, mock_run_command):
        """Opening VS Code should report success when the command succeeds."""
        await self.actions._open_vscode()

        self.actions.console.print.assert_called_with("[green]✓ Opened in VS Code[/green]")
        mock_run_command.assert_called_once_with(["code", str(self.project_path)])

    @patch("fwen.actions.run_command", return_value=(False, "", "missing code"))
    async def test_open_vscode_failure(self, mock_run_command):
        """Opening VS Code should report stderr when the command fails."""
        await self.actions._open_vscode()

        self.actions.console.print.assert_called_with(
            "[yellow]⚠ Could not open VS Code: missing code[/yellow]"
        )
        mock_run_command.assert_called_once_with(["code", str(self.project_path)])

    @patch("fwen.actions.run_command")
    async def test_open_android_studio_uses_fallback(self, mock_run_command):
        """The IDE opener should try both commands until one succeeds."""
        mock_run_command.side_effect = [(False, "", ""), (True, "", "")]

        await self.actions._open_android_studio()

        self.assertEqual(mock_run_command.call_count, 2)
        self.actions.console.print.assert_called_with("[green]✓ Opened in IDE[/green]")

    @patch("fwen.actions.run_command", side_effect=[(False, "", ""), (False, "", "")])
    async def test_open_android_studio_failure(self, mock_run_command):
        """If both IDE commands fail, the user should be warned."""
        await self.actions._open_android_studio()

        self.assertEqual(mock_run_command.call_count, 2)
        self.actions.console.print.assert_called_with(
            "[yellow]⚠ Could not open IDE. Please open manually.[/yellow]"
        )

    @patch("fwen.actions.get_connected_devices", return_value=[])
    async def test_run_app_without_devices(self, mock_get_devices):
        """Running without devices should warn and stop."""
        await self.actions._run_app()

        self.actions.console.print.assert_called_with(
            "[yellow]⚠ No devices found. Please connect a device or start an emulator.[/yellow]"
        )
        mock_get_devices.assert_called_once()

    @patch("fwen.actions.subprocess.run")
    @patch("fwen.actions.get_connected_devices")
    async def test_run_app_on_selected_device(self, mock_get_devices, mock_subprocess_run):
        """When multiple devices exist, the selected one should be used."""
        mock_get_devices.return_value = [
            {"id": "ios-sim", "name": "iPhone 16"},
            {"id": "android-emulator", "name": "Pixel 9"},
        ]

        with patch("fwen.actions.questionary.select", return_value=PromptStub("android-emulator")):
            await self.actions._run_app()

        mock_subprocess_run.assert_called_once_with(
            ["flutter", "run", "-d", "android-emulator"],
            cwd=str(self.project_path),
        )

    @patch("fwen.actions.subprocess.run")
    @patch("fwen.actions.get_connected_devices", return_value=[{"id": "ios-sim", "name": "iPhone 16"}])
    async def test_run_app_on_single_device(self, mock_get_devices, mock_subprocess_run):
        """When exactly one device exists, it should be used without prompting."""
        await self.actions._run_app()

        self.actions.console.print.assert_any_call("[cyan]Running on iPhone 16...[/cyan]")
        mock_subprocess_run.assert_called_once_with(
            ["flutter", "run", "-d", "ios-sim"],
            cwd=str(self.project_path),
        )

    async def test_create_feature_missing_script(self):
        """Feature creation should stop when the script is unavailable."""
        with patch.object(self.actions, "_get_feature_script_path", return_value=Path("/tmp/missing.py")):
            await self.actions._create_feature()

        self.actions.console.print.assert_called_with("[red]✗ feature-dev.py script not found[/red]")

    @patch("fwen.actions.run_command", return_value=(True, "", ""))
    async def test_create_feature_success(self, mock_run_command):
        """Feature creation should invoke the script and print success."""
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "feature-dev.py"
            script_path.write_text("print('ok')\n")

            with (
                patch.object(self.actions, "_get_feature_script_path", return_value=script_path),
                patch("fwen.actions.questionary.text", return_value=PromptStub("Auth")),
            ):
                await self.actions._create_feature()

        mock_run_command.assert_called_once_with(
            ["python3", str(script_path), "Auth"],
            cwd=str(self.project_path),
        )
        self.actions.console.print.assert_called_with("[green]✓ Feature 'Auth' created[/green]")

    @patch("fwen.actions.questionary.text", return_value=PromptStub(""))
    async def test_create_feature_stops_when_name_is_empty(self, mock_text):
        """Feature creation should stop if the prompt returns an empty name."""
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "feature-dev.py"
            script_path.write_text("print('ok')\n")

            with patch.object(self.actions, "_get_feature_script_path", return_value=script_path):
                await self.actions._create_feature()

        self.actions.console.print.assert_not_called()

    @patch("fwen.actions.run_command", return_value=(False, "", "script failed"))
    async def test_create_feature_failure(self, mock_run_command):
        """Feature creation should print stderr when the script fails."""
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "feature-dev.py"
            script_path.write_text("print('ok')\n")

            with (
                patch.object(self.actions, "_get_feature_script_path", return_value=script_path),
                patch("fwen.actions.questionary.text", return_value=PromptStub("Auth")),
            ):
                await self.actions._create_feature()

        mock_run_command.assert_called_once()
        self.actions.console.print.assert_called_with("[red]✗ Failed to create feature: script failed[/red]")

    @patch("fwen.actions.print_tree")
    async def test_show_tree_existing_lib(self, mock_print_tree):
        """Tree display should render the lib directory when present."""
        with patch("pathlib.Path.exists", return_value=True):
            await self.actions._show_tree()

        mock_print_tree.assert_called_once()

    async def test_show_tree_missing_lib(self):
        """Tree display should warn when lib/ is missing."""
        with patch("pathlib.Path.exists", return_value=False):
            await self.actions._show_tree()

        self.actions.console.print.assert_any_call("[yellow]lib/ directory not found[/yellow]")


class TestRunPostCreationActions(unittest.IsolatedAsyncioTestCase):
    """Wrapper tests for the module-level post-creation helper."""

    @patch("fwen.actions.PostCreationActions")
    async def test_run_post_creation_actions_wrapper(self, mock_actions_cls):
        """The wrapper should render the success panel then open the action menu."""
        actions = mock_actions_cls.return_value
        actions.run_action_menu = AsyncMock()

        await run_post_creation_actions(Path("/tmp/project"), {"project_name": "demo"})

        mock_actions_cls.assert_called_once_with(Path("/tmp/project"), {"project_name": "demo"})
        actions.show_success_message.assert_called_once()
        actions.run_action_menu.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
