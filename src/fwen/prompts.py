"""
Interactive prompts for Flutter Clean CLI.
Uses questionary for rich terminal UI.
"""

from pathlib import Path
from typing import Any

import questionary

from .config import Config


class Prompts:
    """Handles all interactive prompts for the CLI."""

    def __init__(self, config: Config):
        """Initialize prompts with config."""
        self.config = config
        self.current_section = 0
        self.total_sections = 5

    def _show_progress(self, section_name: str) -> None:
        """Display progress indicator."""
        self.current_section += 1
        print(f"\n📋 [{self.current_section}/{self.total_sections}] {section_name}\n")

    async def run_all_prompts(self) -> dict[str, Any]:
        """Run all prompt sections sequentially."""
        result = {}

        # Section 1: Project Basics
        self._show_progress("Project Basics")
        result.update(await self._project_basics())

        # Section 2: Architecture & State Management
        self._show_progress("Architecture & State Management")
        result.update(await self._architecture_prompts())

        # Section 3: Platforms & Features
        self._show_progress("Platforms & Features")
        result.update(await self._platforms_prompts())

        # Section 4: Development Tools
        self._show_progress("Development Tools")
        result.update(await self._development_tools_prompts())

        # Section 5: First Feature
        self._show_progress("First Feature")
        result.update(await self._feature_prompt())

        return result

    async def _project_basics(self) -> dict[str, Any]:
        """Section 1: Project basic information."""
        result = {}

        # Project name with validation
        while True:
            name = await questionary.text(
                "Project name (snake_case):",
                validate=lambda x: len(x) > 0 or "Project name is required",
            ).ask_async()

            is_valid, error = self.config.validate_project_name(name)
            if is_valid:
                result["project_name"] = name
                break
            print(f"❌ {error}")

        # Organization ID
        result["org_id"] = await questionary.text(
            "Organization ID (reverse domain):",
            default=self.config.DEFAULTS["org_id"],
        ).ask_async()

        # Description
        result["description"] = await questionary.text(
            "Project description:",
            default=self.config.DEFAULTS["description"],
        ).ask_async()

        # Output directory
        output_dir = await questionary.path(
            "Output directory:",
            default=str(Path.cwd().absolute()),
        ).ask_async()
        result["output_dir"] = output_dir

        return result

    async def _architecture_prompts(self) -> dict[str, Any]:
        """Section 2: Architecture and state management choices."""
        result = {}

        # State management
        result["state_management"] = await questionary.select(
            "Choose state management:",
            choices=[
                questionary.Choice("Bloc", "bloc", description="Recommended for large apps"),
                questionary.Choice("Provider", "provider", description="Simple and flexible"),
                questionary.Choice("Riverpod", "riverpod", description="Modern, type-safe"),
            ],
            default=self.config.DEFAULTS["state_management"],
        ).ask_async()

        # Navigation
        result["navigation"] = await questionary.select(
            "Choose navigation:",
            choices=[
                questionary.Choice("GoRouter", "go_router", description="Declarative routing"),
                questionary.Choice("AutoRoute", "auto_route", description="Code generation routing"),
                questionary.Choice("Navigator 2.0", "navigator", description="Low-level API"),
            ],
            default=self.config.DEFAULTS["navigation"],
        ).ask_async()

        # Dependency injection
        result["dependency_injection"] = await questionary.select(
            "Choose dependency injection:",
            choices=[
                questionary.Choice("GetIt", "get_it", description="Service locator pattern"),
                questionary.Choice("Provider", "provider", description="Inherited widget pattern"),
                questionary.Choice("Riverpod", "riverpod", description="Modern provider pattern"),
            ],
            default=self.config.DEFAULTS["dependency_injection"],
        ).ask_async()

        # Include example code
        result["include_examples"] = await questionary.confirm(
            "Include example code?",
            default=self.config.DEFAULTS["include_examples"],
        ).ask_async()

        return result

    async def _platforms_prompts(self) -> dict[str, Any]:
        """Section 3: Platforms and Firebase configuration."""
        result = {}

        # Platforms
        result["platforms"] = await questionary.checkbox(
            "Select target platforms:",
            choices=[
                questionary.Choice("iOS", "ios", checked=True),
                questionary.Choice("Android", "android", checked=True),
                questionary.Choice("Web", "web"),
                questionary.Choice("macOS", "macos"),
                questionary.Choice("Windows", "windows"),
                questionary.Choice("Linux", "linux"),
            ],
            validate=lambda x: len(x) > 0 or "Select at least one platform",
        ).ask_async()

        # Authentication
        include_auth = await questionary.confirm(
            "Include authentication?",
            default=False,
        ).ask_async()
        result["include_auth"] = include_auth

        if include_auth:
            result["auth_methods"] = await questionary.checkbox(
                "Select authentication methods:",
                choices=[
                    questionary.Choice("Email/Password", "email"),
                    questionary.Choice("Google", "google"),
                    questionary.Choice("Apple", "apple"),
                    questionary.Choice("Phone", "phone"),
                ],
                validate=lambda x: len(x) > 0 or "Select at least one method",
            ).ask_async()

        # Firebase
        include_firebase = await questionary.confirm(
            "Include Firebase?",
            default=False,
        ).ask_async()
        result["include_firebase"] = include_firebase

        if include_firebase:
            result["firebase_services"] = await questionary.checkbox(
                "Select Firebase services:",
                choices=[
                    questionary.Choice("Authentication", "auth"),
                    questionary.Choice("Cloud Firestore", "firestore"),
                    questionary.Choice("Cloud Functions", "functions"),
                    questionary.Choice("Analytics", "analytics"),
                    questionary.Choice("Cloud Messaging", "messaging"),
                    questionary.Choice("Storage", "storage"),
                    questionary.Choice("Remote Config", "remote_config"),
                    questionary.Choice("Crashlytics", "crashlytics"),
                ],
            ).ask_async()

        return result

    async def _development_tools_prompts(self) -> dict[str, Any]:
        """Section 4: Development tools and integrations."""
        result = {}

        # API layer
        include_api = await questionary.confirm(
            "Include API layer?",
            default=False,
        ).ask_async()
        result["include_api"] = include_api

        if include_api:
            result["api_choice"] = await questionary.select(
                "Choose HTTP client:",
                choices=[
                    questionary.Choice("Dio", "dio", description="Powerful HTTP client"),
                    questionary.Choice("Retrofit", "retrofit", description="Type-safe API with codegen"),
                    questionary.Choice("Fetch", "fetch", description="Simple HTTP client"),
                ],
            ).ask_async()

        # State persistence
        include_persistence = await questionary.confirm(
            "Include state persistence?",
            default=False,
        ).ask_async()
        result["include_persistence"] = include_persistence

        if include_persistence:
            result["persistence_choice"] = await questionary.select(
                "Choose persistence solution:",
                choices=[
                    questionary.Choice("Shared Preferences", "shared_preferences", description="Simple key-value"),
                    questionary.Choice("Hive", "hive", description="Fast, lightweight NoSQL"),
                    questionary.Choice("Isar", "isar", description="Fast object database"),
                ],
            ).ask_async()

        # Analytics
        include_analytics = await questionary.confirm(
            "Include analytics?",
            default=False,
        ).ask_async()
        result["include_analytics"] = include_analytics

        if include_analytics:
            result["analytics_choice"] = await questionary.select(
                "Choose analytics service:",
                choices=[
                    questionary.Choice("Firebase Analytics", "firebase_analytics"),
                    questionary.Choice("Sentry", "sentry", description="Error tracking and monitoring"),
                    questionary.Choice("Mixpanel", "mixpanel", description="Product analytics"),
                ],
            ).ask_async()

        # Testing
        include_testing = await questionary.confirm(
            "Include testing setup?",
            default=False,
        ).ask_async()
        result["include_testing"] = include_testing

        if include_testing:
            result["testing_types"] = await questionary.checkbox(
                "Select testing types:",
                choices=[
                    questionary.Choice("Unit tests", "unit"),
                    questionary.Choice("Widget tests", "widget"),
                    questionary.Choice("Integration tests", "integration"),
                ],
                validate=lambda x: len(x) > 0 or "Select at least one testing type",
            ).ask_async()

        # CI/CD
        include_ci = await questionary.confirm(
            "Include CI/CD configuration?",
            default=False,
        ).ask_async()
        result["include_ci"] = include_ci

        if include_ci:
            result["ci_choice"] = await questionary.select(
                "Choose CI/CD platform:",
                choices=[
                    questionary.Choice("GitHub Actions", "github_actions"),
                    questionary.Choice("GitLab CI", "gitlab_ci"),
                    questionary.Choice("None", "none"),
                ],
            ).ask_async()

        return result

    async def _feature_prompt(self) -> dict[str, Any]:
        """Section 5: Initial feature creation."""
        result = {}

        create_feature = await questionary.confirm(
            "Create an initial feature?",
            default=False,
        ).ask_async()
        result["create_feature"] = create_feature

        if create_feature:
            result["feature_name"] = await questionary.text(
                "Feature name (PascalCase, e.g., Auth, Home):",
                validate=lambda x: len(x) > 0 or "Feature name is required",
            ).ask_async()

        return result

    async def confirm_summary(self, config: dict[str, Any]) -> bool:
        """Display summary and ask for confirmation."""
        from rich.console import Console
        from rich.table import Table

        console = Console()

        console.print("\n📝 [bold]Project Configuration Summary[/bold]\n")

        # Create summary table
        table = Table(show_header=False, box=None)
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="green")

        # Basic info
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

        return await questionary.confirm(
            "\nProceed with project creation?",
            default=True,
        ).ask_async()


async def collect_user_config(config: Config) -> dict[str, Any]:
    """Collect all user configuration through interactive prompts."""
    prompts = Prompts(config)
    user_config = await prompts.run_all_prompts()
    return user_config
