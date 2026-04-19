"""
Configuration module for Flutter Clean CLI.
Handles default values, validation, and config management.
"""

import re
from typing import Any


class Config:
    """Manages CLI configuration with defaults and validation."""

    # Default values
    DEFAULTS: dict[str, Any] = {
        "org_id": "com.example",
        "description": "A new Flutter project with Clean Architecture",
        "output_dir": ".",
        "state_management": "bloc",
        "navigation": "go_router",
        "dependency_injection": "get_it",
        "include_examples": True,
        "platforms": ["ios", "android"],
        "include_auth": False,
        "include_firebase": False,
        "include_api": False,
        "include_persistence": False,
        "include_analytics": False,
        "include_testing": False,
        "include_ci": False,
        "create_feature": False,
    }

    # Valid options for select fields
    STATE_MANAGEMENT_OPTIONS = ["bloc", "provider", "riverpod"]
    NAVIGATION_OPTIONS = ["go_router", "auto_route", "navigator"]
    DI_OPTIONS = ["get_it", "provider", "riverpod"]
    PLATFORM_OPTIONS = ["ios", "android", "web", "macos", "windows", "linux"]
    AUTH_METHODS = ["email", "google", "apple", "phone"]
    API_OPTIONS = ["dio", "retrofit", "fetch"]
    PERSISTENCE_OPTIONS = ["shared_preferences", "hive", "isar"]
    ANALYTICS_OPTIONS = ["firebase_analytics", "sentry", "mixpanel"]
    TESTING_OPTIONS = ["unit", "widget", "integration"]
    CI_OPTIONS = ["github_actions", "gitlab_ci", "none"]

    # Firebase services
    FIREBASE_SERVICES = [
        "auth", "firestore", "functions", "analytics",
        "messaging", "storage", "remote_config", "crashlytics"
    ]

    def __init__(self):
        """Initialize config with defaults."""
        self.data: dict[str, Any] = self.DEFAULTS.copy()

    def set(self, key: str, value: Any) -> None:
        """Set a config value."""
        self.data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a config value."""
        return self.data.get(key, default)

    def update(self, updates: dict[str, Any]) -> None:
        """Update multiple config values."""
        self.data.update(updates)

    def validate_project_name(self, name: str) -> tuple[bool, str]:
        """
        Validate Flutter project name.
        Returns (is_valid, error_message).
        """
        if not name:
            return False, "Project name cannot be empty"

        if not re.match(r'^[a-z][a-z0-9_]*$', name):
            return False, (
                "Project name must be lowercase, start with a letter, "
                "and contain only letters, numbers, and underscores"
            )

        if len(name) > 50:
            return False, "Project name must be 50 characters or less"

        return True, ""

    def to_pascal_case(self, snake_str: str) -> str:
        """Convert snake_case to PascalCase."""
        return ''.join(word.capitalize() for word in snake_str.split('_'))

    def to_camel_case(self, snake_str: str) -> str:
        """Convert snake_case to camelCase."""
        parts = snake_str.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    def get_substitution_vars(self) -> dict[str, str]:
        """Get all substitution variables for templates."""
        project_name = self.get("project_name", "")
        return {
            "project_name": project_name,
            "ProjectName": self.to_pascal_case(project_name),
            "projectName": self.to_camel_case(project_name),
            "org_id": self.get("org_id", "com.example"),
            "description": self.get("description", ""),
            "state_management": self.get("state_management", "bloc"),
            "navigation": self.get("navigation", "go_router"),
        }

    def get_pubspec_dependencies(self) -> dict[str, str]:
        """Get dependencies to add to pubspec.yaml based on config."""
        deps = {}

        # State management
        sm = self.get("state_management")
        if sm == "bloc":
            deps.update({
                "flutter_bloc": "^8.1.0",
                "bloc": "^8.1.0",
            })
        elif sm == "provider":
            deps["provider"] = "^6.1.0"
        elif sm == "riverpod":
            deps.update({
                "flutter_riverpod": "^2.4.0",
                "riverpod_annotation": "^2.3.0",
            })

        # Navigation
        nav = self.get("navigation")
        if nav == "go_router":
            deps["go_router"] = "^13.0.0"
        elif nav == "auto_route":
            deps["auto_route"] = "^7.9.0"

        # Dependency injection
        di = self.get("dependency_injection")
        if di == "get_it":
            deps["get_it"] = "^7.6.0"

        # API layer
        if self.get("include_api"):
            api = self.get("api_choice")
            if api == "dio":
                deps["dio"] = "^5.4.0"
            elif api == "retrofit":
                deps.update({
                    "dio": "^5.4.0",
                    "retrofit": "^4.0.0",
                })

        # State persistence
        if self.get("include_persistence"):
            persist = self.get("persistence_choice")
            if persist == "shared_preferences":
                deps["shared_preferences"] = "^2.2.0"
            elif persist == "hive":
                deps["hive"] = "^2.2.0"
            elif persist == "isar":
                deps["isar"] = "^3.1.0"

        # Analytics
        if self.get("include_analytics"):
            analytics = self.get("analytics_choice")
            if analytics == "firebase_analytics":
                deps["firebase_analytics"] = "^10.7.0"
            elif analytics == "sentry":
                deps["sentry_flutter"] = "^7.10.0"
            elif analytics == "mixpanel":
                deps["mixpanel_flutter"] = "^2.2.0"

        # Firebase
        if self.get("include_firebase"):
            deps["firebase_core"] = "^2.24.0"

        # Dev dependencies
        dev_deps = {}
        if nav == "auto_route":
            dev_deps["auto_route_generator"] = "^7.9.0"
        if self.get("include_api") and self.get("api_choice") == "retrofit":
            dev_deps["json_serializable"] = "^6.7.0"
            dev_deps["retrofit_generator"] = "^8.0.0"
        if sm == "riverpod":
            dev_deps["riverpod_generator"] = "^2.3.0"
            dev_deps["riverpod_lint"] = "^2.3.0"
            dev_deps["custom_lint"] = "^0.5.0"

        return {"dependencies": deps, "dev_dependencies": dev_deps}

    def get_selected_platforms(self) -> list[str]:
        """Get list of selected platforms."""
        return self.get("platforms", ["ios", "android"])

    def get_selected_firebase_services(self) -> list[str]:
        """Get list of selected Firebase services."""
        return self.get("firebase_services", [])

    def get_selected_testing_types(self) -> list[str]:
        """Get list of selected testing types."""
        return self.get("testing_types", [])
