#!/usr/bin/env python3
"""
fwen - Flutter Clean Architecture Scaffolder

Create Flutter applications with Clean Architecture from scratch.
Supports both interactive and non-interactive modes.
"""

import asyncio
import sys
from pathlib import Path

from rich.console import Console

from fwen.actions import run_post_creation_actions
from fwen.cli import (
    args_to_config,
    parse_args,
    should_use_interactive_mode,
    validate_args,
)
from fwen.config import Config
from fwen.generator import generate_project
from fwen.prompts import Prompts, collect_user_config
from fwen.template_registry import get_template_registry, iter_selected_templates
from fwen.utils import check_flutter_installed


def print_banner(console: Console, show_banner: bool = True) -> None:
    """Print the CLI banner."""
    if not show_banner:
        return

    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   fwen - Flutter Clean Architecture Scaffolder               ║
║                                                               ║
║   Create Flutter apps with Clean Architecture from scratch    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
    console.print(banner, style="bold cyan")


def print_error(console: Console, message: str) -> None:
    """Print an error message."""
    console.print(f"\n[red]✗ Error: {message}[/red]\n")


def print_info(console: Console, message: str) -> None:
    """Print an info message."""
    console.print(f"\n[blue]ℹ {message}[/blue]\n")


def print_success(console: Console, message: str) -> None:
    """Print a success message."""
    console.print(f"\n[green]✓ {message}[/green]\n")


def print_config_summary(console: Console, config: dict) -> None:
    """Print configuration summary."""
    from rich.table import Table

    table = Table(show_header=False, box=None)
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Project Name", config.get("project_name", ""))
    table.add_row("Organization", config.get("org_id", ""))
    table.add_row("State Management", config.get("state_management", ""))
    table.add_row("Navigation", config.get("navigation", ""))
    table.add_row("Platforms", ", ".join(config.get("platforms", [])))

    if config.get("include_firebase"):
        table.add_row("Firebase", ", ".join(config.get("firebase_services", [])))

    if config.get("create_feature"):
        table.add_row("Initial Feature", config.get("feature_name", ""))

    console.print(table)


def is_template_command(args) -> bool:
    """Return whether args requests template registry command mode."""
    return getattr(args, "command", None) == "templates"


def _format_dependencies(template) -> str:
    """Render CLI dependency list for display."""
    if not template.cli_dependencies:
        return "always"
    return ", ".join(template.cli_dependencies)


def _format_exclusions(template) -> str:
    """Render mutual exclusion list for display."""
    if not template.mutually_exclusive_with:
        return "-"
    return ", ".join(template.mutually_exclusive_with)


def _selection_reason(template, selected_ids: set[str]) -> str:
    """Explain selection status for a template row."""
    if template.template_id in selected_ids:
        return "selected"
    if not template.applies_during_generation:
        return "feature-script-only"
    return "requirements-not-met"


def run_template_command(args, console: Console) -> None:
    """Render template registry information."""
    from rich.table import Table

    action = args.template_action or "list"

    if action == "list":
        table = Table(title="Template Registry")
        table.add_column("Template ID", style="cyan")
        table.add_column("Layer", style="green")
        table.add_column("Status")
        table.add_column("CLI Dependencies")
        table.add_column("Output Path")

        for template in get_template_registry():
            table.add_row(
                template.template_id,
                template.layer,
                template.status,
                _format_dependencies(template),
                template.output_path,
            )
        console.print(table)
        return

    config = Config()
    config.update(args_to_config(args))
    selected = iter_selected_templates(config)
    selected_ids = {template.template_id for template in selected}

    console.print("[bold]Template Selection[/bold]")
    console.print(
        "Config: "
        f"state_management={config.get('state_management')}, "
        f"navigation={config.get('navigation')}, "
        f"include_examples={config.get('include_examples')}, "
        f"include_testing={config.get('include_testing')}"
    )

    table = Table(title="Template Explain")
    table.add_column("Template ID", style="cyan")
    table.add_column("Selected")
    table.add_column("Reason")
    table.add_column("Mutually Exclusive With")

    for template in get_template_registry():
        table.add_row(
            template.template_id,
            "yes" if template.template_id in selected_ids else "no",
            _selection_reason(template, selected_ids),
            _format_exclusions(template),
        )
    console.print(table)


async def run_non_interactive_mode(args, console: Console, config: Config, templates_dir: Path):
    """Run CLI in non-interactive mode with command-line arguments."""
    # Convert args to config
    user_config = args_to_config(args)
    config.update(user_config)

    # Print what we're creating
    console.print("[bold]Creating Flutter project with the following configuration:[/bold]\n")
    print_config_summary(console, config.data)

    # Confirm unless --yes flag is set
    if not args.yes:
        console.print("\n[yellow]Proceed with project creation?[/yellow] ", end="")
        try:
            # Simple input for non-interactive mode
            response = input("[Y/n]: ").strip().lower()
            if response and response not in ["y", "yes"]:
                console.print("\n[yellow]Cancelled.[/yellow]\n")
                sys.exit(0)
        except (EOFError, KeyboardInterrupt):
            console.print("\n\n[yellow]Cancelled.[/yellow]\n")
            sys.exit(0)

    console.print("\n[bold cyan]Creating project...[/bold cyan]\n")

    # Generate project
    success, message, project_path = generate_project(config, templates_dir)

    if not success:
        print_error(console, message)
        sys.exit(1)

    print_success(console, message)

    # In non-interactive mode, just print next steps instead of showing menu
    console.print("\n[bold]Next steps:[/bold]")
    console.print(f"  cd {project_path}")
    console.print("  flutter pub get")
    console.print("  flutter run\n")


async def run_interactive_mode(console: Console, config: Config, templates_dir: Path):
    """Run CLI in interactive mode with prompts."""
    console.print("[bold]Let's configure your Flutter project![/bold]\n")
    console.print("[dim]Press Ctrl+C at any time to cancel.[/dim]\n")

    user_config = await collect_user_config(config)
    config.update(user_config)

    # Show summary and confirm
    prompts = Prompts(config)
    confirmed = await prompts.confirm_summary(config.data)

    if not confirmed:
        console.print("\n[yellow]Cancelled.[/yellow]\n")
        sys.exit(0)

    # Generate project
    console.print("\n[bold cyan]Creating project...[/bold cyan]\n")

    success, message, project_path = generate_project(config, templates_dir)

    if not success:
        print_error(console, message)
        sys.exit(1)

    # Run post-creation actions
    await run_post_creation_actions(project_path, config.data)


async def main():
    """Main entry point."""
    # Parse command-line arguments
    args = parse_args()

    console = Console()

    if is_template_command(args):
        run_template_command(args, console)
        return

    # Check Flutter installation
    console.print("[dim]Checking Flutter installation...[/dim]")
    flutter_ok, flutter_msg = check_flutter_installed()
    if not flutter_ok:
        print_error(console, f"Flutter not found: {flutter_msg}")
        print_info(console, "Please install Flutter and ensure it's in your PATH.")
        sys.exit(1)
    console.print("[green]✓ Flutter detected[/green]\n")

    # Initialize config
    config = Config()
    templates_dir = Path(__file__).parent.parent.parent / "templates"

    # Check templates directory
    if not templates_dir.exists():
        print_error(console, f"Templates directory not found: {templates_dir}")
        print_info(console, "Please ensure you're running from the correct location.")
        sys.exit(1)

    # Validate arguments if in non-interactive mode
    if not should_use_interactive_mode(args):
        is_valid, error = validate_args(args)
        if not is_valid:
            print_error(console, error)
            sys.exit(1)

    # Determine mode and run
    interactive = should_use_interactive_mode(args)

    try:
        # Show banner only in interactive mode
        print_banner(console, show_banner=interactive)

        if interactive:
            await run_interactive_mode(console, config, templates_dir)
        else:
            await run_non_interactive_mode(args, console, config, templates_dir)

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Cancelled by user.[/yellow]\n")
        sys.exit(0)
    except Exception as e:
        print_error(console, str(e))
        import traceback

        console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
