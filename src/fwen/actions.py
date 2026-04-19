"""
Post-creation actions for Flutter Clean CLI.
Handles follow-up commands after project generation.
"""

import subprocess
from pathlib import Path

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .utils import get_connected_devices, get_flutter_executable, print_tree, run_command


class PostCreationActions:
    """Manages post-creation action menu and execution."""

    def __init__(self, project_path: Path, config: dict):
        """Initialize with project path and configuration."""
        self.project_path = project_path
        self.config = config
        self.console = Console()

    def show_success_message(self) -> None:
        """Display success message with project summary."""
        project_name = self.config.get("project_name", "")
        state_management = self.config.get("state_management", "")
        navigation = self.config.get("navigation", "")
        platforms = self.config.get("platforms", [])

        summary = Text()
        summary.append("✨ Flutter project '", style="bold green")
        summary.append(project_name, style="bold cyan")
        summary.append("' created successfully!\n\n", style="bold green")

        summary.append("Location: ", style="dim")
        summary.append(f"{self.project_path}\n", style="cyan")
        summary.append("State Management: ", style="dim")
        summary.append(f"{state_management}\n", style="cyan")
        summary.append("Navigation: ", style="dim")
        summary.append(f"{navigation}\n", style="cyan")
        summary.append("Platforms: ", style="dim")
        summary.append(f"{', '.join(platforms)}\n", style="cyan")

        if self.config.get("include_firebase"):
            services = self.config.get("firebase_services", [])
            summary.append("Firebase: ", style="dim")
            summary.append(f"{', '.join(services)}\n", style="cyan")

        panel = Panel(
            summary,
            title="[bold green]Success[/bold green]",
            border_style="green",
        )

        self.console.print(panel)

    def _get_feature_script_path(self) -> Path:
        """Get the bundled feature generator script path."""
        return Path(__file__).parent.parent.parent / "scripts" / "feature-dev.py"

    async def run_action_menu(self) -> None:
        """Display and execute post-creation action menu."""
        while True:
            choices = [
                questionary.Choice("📦 Run flutter pub get", "pub_get"),
                questionary.Choice("🔨 Run build_runner", "build_runner"),
                questionary.Choice("📝 Open in VS Code", "vscode"),
                questionary.Choice("🔧 Open in Android Studio", "android_studio"),
                questionary.Choice("▶️  Run app on device", "run"),
                questionary.Choice("🎯 Create additional feature", "feature"),
                questionary.Choice("🌳 View project structure", "tree"),
                questionary.Choice("🚪 Exit", "exit"),
            ]

            action = await questionary.select(
                "What would you like to do next?",
                choices=choices,
            ).ask_async()

            if action == "exit":
                break

            await self._execute_action(action)

    async def _execute_action(self, action: str) -> None:
        """Execute a single action."""
        actions = {
            "pub_get": self._flutter_pub_get,
            "build_runner": self._run_build_runner,
            "vscode": self._open_vscode,
            "android_studio": self._open_android_studio,
            "run": self._run_app,
            "feature": self._create_feature,
            "tree": self._show_tree,
        }

        handler = actions.get(action)
        if handler:
            try:
                await handler()
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")

    async def _flutter_pub_get(self) -> None:
        """Run flutter pub get."""
        with self.console.status("[bold cyan]Running flutter pub get...[/bold cyan]"):
            success, stdout, stderr = run_command(
                [get_flutter_executable(), "pub", "get"],
                cwd=str(self.project_path),
                capture_output=False,
            )

        if success:
            self.console.print("[green]✓ Dependencies installed[/green]")
        else:
            self.console.print(f"[red]✗ Failed to install dependencies: {stderr}[/red]")

    async def _run_build_runner(self) -> None:
        """Run dart run build_runner build."""
        self.console.print("[yellow]This may take a few minutes...[/yellow]")

        with self.console.status("[bold cyan]Running build_runner...[/bold cyan]"):
            success, stdout, stderr = run_command(
                ["dart", "run", "build_runner", "build", "--delete-conflicting-outputs"],
                cwd=str(self.project_path),
                capture_output=False,
            )

        if success:
            self.console.print("[green]✓ Code generation complete[/green]")
        else:
            self.console.print(f"[red]✗ Build failed: {stderr}[/red]")

    async def _open_vscode(self) -> None:
        """Open project in VS Code."""
        success, _, stderr = run_command(["code", str(self.project_path)])

        if success:
            self.console.print("[green]✓ Opened in VS Code[/green]")
        else:
            self.console.print(f"[yellow]⚠ Could not open VS Code: {stderr}[/yellow]")

    async def _open_android_studio(self) -> None:
        """Open project in Android Studio / IntelliJ."""
        # Try IntelliJ first, then Android Studio
        commands = [
            ["idea", str(self.project_path)],
            ["studio", str(self.project_path)],
        ]

        opened = False
        for cmd in commands:
            success, _, _ = run_command(cmd, capture_output=False)
            if success:
                opened = True
                self.console.print("[green]✓ Opened in IDE[/green]")
                break

        if not opened:
            self.console.print("[yellow]⚠ Could not open IDE. Please open manually.[/yellow]")

    async def _run_app(self) -> None:
        """Run app on connected device."""
        # Check for connected devices
        devices = get_connected_devices()

        if not devices:
            self.console.print("[yellow]⚠ No devices found. Please connect a device or start an emulator.[/yellow]")
            return

        if len(devices) == 1:
            device_id = devices[0]["id"]
            self.console.print(f"[cyan]Running on {devices[0]['name']}...[/cyan]")
        else:
            # Ask user to select device
            choices = [
                questionary.Choice(f"{d['name']}", d["id"])
                for d in devices
            ]
            device_id = await questionary.select(
                "Select device:",
                choices=choices,
            ).ask_async()

        # Run the app
        self.console.print("[yellow]Starting app... Press 'q' to stop.[/yellow]")

        subprocess.run(
            [get_flutter_executable(), "run", "-d", device_id],
            cwd=str(self.project_path),
        )

    async def _create_feature(self) -> None:
        """Create an additional feature."""
        feature_script = self._get_feature_script_path()

        if not feature_script.exists():
            self.console.print("[red]✗ feature-dev.py script not found[/red]")
            return

        feature_name = await questionary.text(
            "Feature name (PascalCase):",
            validate=lambda x: len(x) > 0 or "Feature name is required",
        ).ask_async()

        if not feature_name:
            return

        with self.console.status(f"[bold cyan]Creating feature '{feature_name}'...[/bold cyan]"):
            success, stdout, stderr = run_command(
                ["python3", str(feature_script), feature_name],
                cwd=str(self.project_path),
            )

        if success:
            self.console.print(f"[green]✓ Feature '{feature_name}' created[/green]")
        else:
            self.console.print(f"[red]✗ Failed to create feature: {stderr}[/red]")

    async def _show_tree(self) -> None:
        """Display project structure."""
        self.console.print("\n[bold]lib/ directory structure:[/bold]\n")
        lib_path = self.project_path / "lib"
        if lib_path.exists():
            print_tree(lib_path, max_depth=3)
        else:
            self.console.print("[yellow]lib/ directory not found[/yellow]")
        print()


async def run_post_creation_actions(project_path: Path, config: dict) -> None:
    """Run the post-creation action menu."""
    actions = PostCreationActions(project_path, config)
    actions.show_success_message()
    await actions.run_action_menu()
