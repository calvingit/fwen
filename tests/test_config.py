"""
Unit tests for the Config module.
"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for Config class."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = Config()

    def test_default_values(self):
        """Test that default values are set correctly."""
        self.assertEqual(self.config.get("org_id"), "com.example")
        self.assertEqual(self.config.get("state_management"), "bloc")
        self.assertEqual(self.config.get("navigation"), "go_router")
        self.assertEqual(self.config.get("dependency_injection"), "get_it")
        self.assertTrue(self.config.get("include_examples"))

    def test_set_and_get(self):
        """Test setting and getting config values."""
        self.config.set("project_name", "test_project")
        self.assertEqual(self.config.get("project_name"), "test_project")

        self.config.set("org_id", "com.mycompany")
        self.assertEqual(self.config.get("org_id"), "com.mycompany")

    def test_get_with_default(self):
        """Test getting values with default fallback."""
        self.assertIsNone(self.config.get("nonexistent"))
        self.assertEqual(self.config.get("nonexistent", "default"), "default")

    def test_update(self):
        """Test updating multiple values at once."""
        updates = {
            "project_name": "my_app",
            "org_id": "com.example",
            "state_management": "provider",
        }
        self.config.update(updates)

        self.assertEqual(self.config.get("project_name"), "my_app")
        self.assertEqual(self.config.get("state_management"), "provider")

    def test_validate_project_name_valid(self):
        """Test validation of valid project names."""
        test_cases = [
            "my_app",
            "my_test_app",
            "app",
            "my_app_123",
            "a",  # Minimum length
        ]

        for name in test_cases:
            is_valid, error = self.config.validate_project_name(name)
            self.assertTrue(is_valid, f"Name '{name}' should be valid: {error}")

    def test_validate_project_name_invalid(self):
        """Test validation of invalid project names."""
        test_cases = [
            ("", "empty name"),
            ("MyApp", "uppercase"),
            ("my-App", "contains hyphen"),
            ("my.App", "contains dot"),
            ("my App", "contains space"),
            ("123app", "starts with number"),
            ("_app", "starts with underscore"),
            ("a" * 51, "too long"),
        ]

        for name, reason in test_cases:
            is_valid, error = self.config.validate_project_name(name)
            self.assertFalse(is_valid, f"Name '{name}' should be invalid ({reason})")

    def test_to_pascal_case(self):
        """Test conversion to PascalCase."""
        test_cases = [
            ("my_app", "MyApp"),
            ("my_test_app", "MyTestApp"),
            ("app", "App"),
            ("my_awesome_flutter_app", "MyAwesomeFlutterApp"),
        ]

        for input_val, expected in test_cases:
            result = self.config.to_pascal_case(input_val)
            self.assertEqual(result, expected)

    def test_to_camel_case(self):
        """Test conversion to camelCase."""
        test_cases = [
            ("my_app", "myApp"),
            ("my_test_app", "myTestApp"),
            ("app", "app"),
            ("my_awesome_flutter_app", "myAwesomeFlutterApp"),
        ]

        for input_val, expected in test_cases:
            result = self.config.to_camel_case(input_val)
            self.assertEqual(result, expected)

    def test_get_substitution_vars(self):
        """Test generation of substitution variables."""
        self.config.set("project_name", "my_test_app")
        self.config.set("org_id", "com.example")
        self.config.set("description", "Test app")

        vars = self.config.get_substitution_vars()

        self.assertEqual(vars["project_name"], "my_test_app")
        self.assertEqual(vars["ProjectName"], "MyTestApp")
        self.assertEqual(vars["projectName"], "myTestApp")
        self.assertEqual(vars["org_id"], "com.example")
        self.assertEqual(vars["description"], "Test app")

    def test_get_pubspec_dependencies_bloc(self):
        """Test dependency generation for Bloc state management."""
        self.config.set("state_management", "bloc")
        deps = self.config.get_pubspec_dependencies()

        self.assertIn("flutter_bloc", deps["dependencies"])
        self.assertIn("bloc", deps["dependencies"])

    def test_get_pubspec_dependencies_provider(self):
        """Test dependency generation for Provider state management."""
        self.config.set("state_management", "provider")
        deps = self.config.get_pubspec_dependencies()

        self.assertIn("provider", deps["dependencies"])

    def test_get_pubspec_dependencies_riverpod(self):
        """Test dependency generation for Riverpod state management."""
        self.config.set("state_management", "riverpod")
        deps = self.config.get_pubspec_dependencies()

        self.assertIn("flutter_riverpod", deps["dependencies"])
        self.assertIn("riverpod_annotation", deps["dependencies"])

    def test_get_pubspec_dependencies_navigation(self):
        """Test dependency generation for different navigation options."""
        # GoRouter
        self.config.set("navigation", "go_router")
        deps = self.config.get_pubspec_dependencies()
        self.assertIn("go_router", deps["dependencies"])

        # AutoRoute
        self.config.set("navigation", "auto_route")
        deps = self.config.get_pubspec_dependencies()
        self.assertIn("auto_route", deps["dependencies"])

    def test_get_pubspec_dependencies_api(self):
        """Test dependency generation for API layer."""
        self.config.set("include_api", True)

        # Dio
        self.config.set("api_choice", "dio")
        deps = self.config.get_pubspec_dependencies()
        self.assertIn("dio", deps["dependencies"])

        # Retrofit
        self.config.set("api_choice", "retrofit")
        deps = self.config.get_pubspec_dependencies()
        self.assertIn("dio", deps["dependencies"])
        self.assertIn("retrofit", deps["dependencies"])

    def test_get_pubspec_dependencies_persistence(self):
        """Test dependency generation for state persistence."""
        self.config.set("include_persistence", True)

        # Shared Preferences
        self.config.set("persistence_choice", "shared_preferences")
        deps = self.config.get_pubspec_dependencies()
        self.assertIn("shared_preferences", deps["dependencies"])

        # Hive
        self.config.set("persistence_choice", "hive")
        deps = self.config.get_pubspec_dependencies()
        self.assertIn("hive", deps["dependencies"])

    def test_get_selected_platforms(self):
        """Test getting selected platforms."""
        self.config.set("platforms", ["ios", "android", "web"])
        platforms = self.config.get_selected_platforms()

        self.assertEqual(platforms, ["ios", "android", "web"])

    def test_get_selected_firebase_services(self):
        """Test getting selected Firebase services."""
        self.config.set("firebase_services", ["auth", "firestore", "analytics"])
        services = self.config.get_selected_firebase_services()

        self.assertEqual(services, ["auth", "firestore", "analytics"])

    def test_get_selected_testing_types(self):
        """Test getting selected testing types."""
        self.config.set("testing_types", ["unit", "widget"])
        types = self.config.get_selected_testing_types()

        self.assertEqual(types, ["unit", "widget"])


if __name__ == "__main__":
    unittest.main()
