"""Unit tests for the template registry."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fwen.config import Config
from fwen.template_registry import get_template_registry, iter_selected_templates


class TestTemplateRegistry(unittest.TestCase):
    """Ensure the template registry remains a stable source of truth."""

    def test_registry_contains_core_connector_and_commerce_scenario(self):
        """The registry should include the new connector and scenario templates."""
        template_ids = {template.template_id for template in get_template_registry()}

        self.assertIn("core.di.feature_registrations", template_ids)
        self.assertIn("scenario.commerce_reference", template_ids)

    def test_selected_templates_include_connectors_and_respect_examples_switch(self):
        """Selection should include connector templates and gate the scenario by include_examples."""
        config = Config()
        config.set("state_management", "provider")
        config.set("navigation", "navigator")
        config.set("include_examples", False)
        selected_without_examples = {
            template.template_id for template in iter_selected_templates(config)
        }

        self.assertIn("base", selected_without_examples)
        self.assertIn("core.di.feature_registrations", selected_without_examples)
        self.assertIn("state_management.provider", selected_without_examples)
        self.assertIn("navigation.navigator", selected_without_examples)
        self.assertNotIn("scenario.commerce_reference", selected_without_examples)

        config.set("include_examples", True)
        selected_with_examples = {
            template.template_id for template in iter_selected_templates(config)
        }
        self.assertIn("scenario.commerce_reference", selected_with_examples)

    def test_state_and_navigation_templates_declare_mutual_exclusions(self):
        """Mutually exclusive template families should declare exclusions in metadata."""
        registry_by_id = {template.template_id: template for template in get_template_registry()}

        self.assertIn(
            "state_management.provider",
            registry_by_id["state_management.bloc"].mutually_exclusive_with,
        )
        self.assertIn(
            "navigation.auto_route",
            registry_by_id["navigation.go_router"].mutually_exclusive_with,
        )


if __name__ == "__main__":
    unittest.main()
