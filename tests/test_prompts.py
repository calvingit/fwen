"""Unit tests for interactive prompt helpers."""

import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

# Add source directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fwen.config import Config
from fwen.prompts import Prompts, collect_user_config


class PromptStub:
    """Simple async prompt stub for questionary helpers."""

    def __init__(self, value):
        self.value = value

    async def ask_async(self):
        return self.value


class TestPrompts(unittest.IsolatedAsyncioTestCase):
    """Tests for the Prompts class."""

    def setUp(self):
        self.config = Config()
        self.prompts = Prompts(self.config)

    def test_show_progress_increments_counter(self):
        """Progress rendering should increment the current section counter."""
        with patch("builtins.print") as mock_print:
            self.prompts._show_progress("Project Basics")

        self.assertEqual(self.prompts.current_section, 1)
        mock_print.assert_called_once()

    async def test_run_all_prompts_combines_all_sections(self):
        """run_all_prompts should merge every section result in order."""
        self.prompts._show_progress = Mock()
        self.prompts._project_basics = AsyncMock(return_value={"project_name": "demo"})
        self.prompts._architecture_prompts = AsyncMock(return_value={"state_management": "bloc"})
        self.prompts._platforms_prompts = AsyncMock(return_value={"platforms": ["ios"]})
        self.prompts._development_tools_prompts = AsyncMock(return_value={"include_api": True})
        self.prompts._feature_prompt = AsyncMock(return_value={"create_feature": False})

        result = await self.prompts.run_all_prompts()

        self.assertEqual(
            result,
            {
                "project_name": "demo",
                "state_management": "bloc",
                "platforms": ["ios"],
                "include_api": True,
                "create_feature": False,
            },
        )
        self.assertEqual(self.prompts._show_progress.call_count, 5)

    @patch("fwen.prompts.questionary.path")
    @patch("fwen.prompts.questionary.text")
    async def test_project_basics_retries_until_project_name_is_valid(self, mock_text, mock_path):
        """Project basics should retry until the project name validates."""
        mock_text.side_effect = [
            PromptStub("InvalidName"),
            PromptStub("demo_app"),
            PromptStub("com.example"),
            PromptStub("Demo app"),
        ]
        mock_path.return_value = PromptStub("/tmp/output")

        with patch.object(
            self.config,
            "validate_project_name",
            side_effect=[(False, "bad name"), (True, "")],
        ):
            with patch("builtins.print") as mock_print:
                result = await self.prompts._project_basics()

        self.assertEqual(
            result,
            {
                "project_name": "demo_app",
                "org_id": "com.example",
                "description": "Demo app",
                "output_dir": "/tmp/output",
            },
        )
        mock_print.assert_any_call("❌ bad name")

    @patch("fwen.prompts.questionary.confirm")
    @patch("fwen.prompts.questionary.select")
    async def test_architecture_prompts_collect_values(self, mock_select, mock_confirm):
        """Architecture prompts should gather state, navigation, DI, and examples."""
        mock_select.side_effect = [
            PromptStub("riverpod"),
            PromptStub("auto_route"),
            PromptStub("provider"),
        ]
        mock_confirm.return_value = PromptStub(False)

        result = await self.prompts._architecture_prompts()

        self.assertEqual(
            result,
            {
                "state_management": "riverpod",
                "navigation": "auto_route",
                "dependency_injection": "provider",
                "include_examples": False,
            },
        )

    @patch("fwen.prompts.questionary.confirm")
    @patch("fwen.prompts.questionary.checkbox")
    async def test_platforms_prompts_include_optional_auth_and_firebase(self, mock_checkbox, mock_confirm):
        """Platforms prompts should include auth and firebase details when enabled."""
        mock_checkbox.side_effect = [
            PromptStub(["ios", "android"]),
            PromptStub(["email", "google"]),
            PromptStub(["auth", "firestore"]),
        ]
        mock_confirm.side_effect = [PromptStub(True), PromptStub(True)]

        result = await self.prompts._platforms_prompts()

        self.assertEqual(
            result,
            {
                "platforms": ["ios", "android"],
                "include_auth": True,
                "auth_methods": ["email", "google"],
                "include_firebase": True,
                "firebase_services": ["auth", "firestore"],
            },
        )

    @patch("fwen.prompts.questionary.confirm")
    @patch("fwen.prompts.questionary.checkbox")
    @patch("fwen.prompts.questionary.select")
    async def test_development_tools_prompts_collect_enabled_options(
        self, mock_select, mock_checkbox, mock_confirm
    ):
        """Development tool prompts should gather selected integrations."""
        mock_confirm.side_effect = [
            PromptStub(True),
            PromptStub(True),
            PromptStub(True),
            PromptStub(True),
            PromptStub(True),
        ]
        mock_select.side_effect = [
            PromptStub("retrofit"),
            PromptStub("hive"),
            PromptStub("sentry"),
            PromptStub("github_actions"),
        ]
        mock_checkbox.return_value = PromptStub(["unit", "widget"])

        result = await self.prompts._development_tools_prompts()

        self.assertEqual(
            result,
            {
                "include_api": True,
                "api_choice": "retrofit",
                "include_persistence": True,
                "persistence_choice": "hive",
                "include_analytics": True,
                "analytics_choice": "sentry",
                "include_testing": True,
                "testing_types": ["unit", "widget"],
                "include_ci": True,
                "ci_choice": "github_actions",
            },
        )

    @patch("fwen.prompts.questionary.confirm")
    @patch("fwen.prompts.questionary.text")
    async def test_feature_prompt_returns_name_when_enabled(self, mock_text, mock_confirm):
        """Feature prompt should include a feature name when the flag is enabled."""
        mock_confirm.return_value = PromptStub(True)
        mock_text.return_value = PromptStub("Auth")

        result = await self.prompts._feature_prompt()

        self.assertEqual(result, {"create_feature": True, "feature_name": "Auth"})

    @patch("fwen.prompts.questionary.confirm")
    async def test_confirm_summary_returns_confirmation(self, mock_confirm):
        """Summary confirmation should return the confirmation answer."""
        mock_confirm.return_value = PromptStub(True)

        with patch("rich.console.Console") as mock_console_cls:
            result = await self.prompts.confirm_summary(
                {
                    "project_name": "demo",
                    "include_firebase": True,
                    "firebase_services": ["auth"],
                    "create_feature": True,
                    "feature_name": "Auth",
                }
            )

        self.assertTrue(result)
        mock_console_cls.return_value.print.assert_called()

    async def test_collect_user_config_delegates_to_prompts(self):
        """The module helper should return the result of run_all_prompts."""
        with patch.object(Prompts, "run_all_prompts", AsyncMock(return_value={"project_name": "demo"})):
            result = await collect_user_config(self.config)

        self.assertEqual(result, {"project_name": "demo"})


if __name__ == "__main__":
    unittest.main()
