"""
Unit tests for the Generator module.
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fwen.config import Config
from fwen.generator import ProjectGenerator, generate_project


class TestProjectGenerator(unittest.TestCase):
    """Test cases for ProjectGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.templates_dir = Path(self.test_dir) / "templates"
        self.output_dir = Path(self.test_dir) / "output"

        # Create template structure
        self.templates_dir.mkdir(parents=True)
        (self.templates_dir / "base" / "lib").mkdir(parents=True)
        (self.templates_dir / "base" / "lib" / "main.dart").write_text(
            "import 'bootstrap.dart';\n\nFuture<void> main() async {\n  await bootstrap();\n}\n"
        )
        (self.templates_dir / "base" / "lib" / "bootstrap.dart").write_text(
            "import 'package:flutter/widgets.dart';\n\n"
            "import 'app/app.dart';\n"
            "import 'core/di/service_locator.dart';\n\n"
            "Future<void> bootstrap() async {\n"
            "  WidgetsFlutterBinding.ensureInitialized();\n"
            "  await configureDependencies();\n"
            "  runApp(const App());\n"
            "}\n"
        )
        (self.templates_dir / "base" / "lib" / "app").mkdir(parents=True, exist_ok=True)
        (self.templates_dir / "base" / "lib" / "app" / "app.dart").write_text(
            "import 'package:flutter/material.dart';\n\n"
            "import '../core/di/service_locator.dart';\n"
            "import '../core/state_management/app_state.dart';\n"
            "import '../shared/themes/app_theme.dart';\n"
            "import 'routes.dart';\n\n"
            "class App extends StatelessWidget {\n"
            "  const App({super.key});\n\n"
            "  @override\n"
            "  Widget build(BuildContext context) {\n"
            "    final controller = appStateController;\n\n"
            "    return AppStateScope(\n"
            "      controller: controller,\n"
            "      child: AnimatedBuilder(\n"
            "        animation: controller,\n"
            "        builder: (context, _) {\n"
            "          return MaterialApp(\n"
            "            title: '{{ProjectName}}',\n"
            "            theme: AppTheme.light(),\n"
            "            darkTheme: AppTheme.dark(),\n"
            "            themeMode: controller.state.themeMode,\n"
            "            initialRoute: AppRoutes.home,\n"
            "            routes: AppRoutes.routes,\n"
            "          );\n"
            "        },\n"
            "      ),\n"
            "    );\n"
            "  }\n"
            "}\n"
        )
        (self.templates_dir / "base" / "lib" / "app" / "routes.dart").write_text(
            "import 'package:flutter/material.dart';\n\n"
            "import 'pages/home_page.dart';\n\n"
            "class AppRoutes {\n"
            "  static const home = '/';\n\n"
            "  static final Map<String, WidgetBuilder> routes = {\n"
            "    home: (context) => const HomePage(),\n"
            "  };\n"
            "}\n"
        )
        (self.templates_dir / "base" / "lib" / "app" / "pages").mkdir(parents=True, exist_ok=True)
        (self.templates_dir / "base" / "lib" / "app" / "pages" / "home_page.dart").write_text(
            "import 'package:flutter/material.dart';\n\n"
            "import '../../core/state_management/app_state.dart';\n\n"
            "class HomePage extends StatelessWidget {\n"
            "  const HomePage({super.key});\n\n"
            "  @override\n"
            "  Widget build(BuildContext context) {\n"
            "    final appStateController = AppStateScope.of(context);\n"
            "    final appState = appStateController.state;\n\n"
            "    return Scaffold(\n"
            "      appBar: AppBar(\n"
            "        title: const Text('{{ProjectName}}'),\n"
            "      ),\n"
            "      body: Center(\n"
            "        child: Text('Theme mode: ${appState.themeMode.name}'),\n"
            "      ),\n"
            "    );\n"
            "  }\n"
            "}\n"
        )
        (self.templates_dir / "base" / "lib" / "core" / "di").mkdir(parents=True, exist_ok=True)
        (self.templates_dir / "base" / "lib" / "core" / "di" / "service_locator.dart").write_text(
            "import 'package:get_it/get_it.dart';\n\n"
            "import '../state_management/app_state.dart';\n\n"
            "final GetIt serviceLocator = GetIt.instance;\n\n"
            "Future<void> configureDependencies() async {\n"
            "  if (!serviceLocator.isRegistered<AppStateController>()) {\n"
            "    serviceLocator.registerSingleton<AppStateController>(\n"
            "      AppStateController(),\n"
            "    );\n"
            "  }\n"
            "}\n"
        )
        (self.templates_dir / "base" / "lib" / "core" / "state_management").mkdir(
            parents=True, exist_ok=True
        )
        (
            self.templates_dir / "base" / "lib" / "core" / "state_management" / "app_state.dart"
        ).write_text(
            "import 'package:flutter/material.dart';\n\n"
            "class AppState {\n"
            "  const AppState({this.themeMode = ThemeMode.system});\n\n"
            "  final ThemeMode themeMode;\n"
            "}\n\n"
            "class AppStateController extends ChangeNotifier {\n"
            "  AppStateController([AppState initialState = const AppState()]) : _state = initialState;\n\n"
            "  AppState _state;\n\n"
            "  AppState get state => _state;\n"
            "}\n\n"
            "class AppStateScope extends InheritedNotifier<AppStateController> {\n"
            "  const AppStateScope({super.key, required AppStateController controller, required super.child})\n"
            "      : super(notifier: controller);\n"
            "}\n"
        )
        (self.templates_dir / "base" / "lib" / "shared" / "themes").mkdir(
            parents=True, exist_ok=True
        )
        (self.templates_dir / "base" / "lib" / "shared" / "themes" / "app_theme.dart").write_text(
            "import 'package:flutter/material.dart';\n\n"
            "class AppTheme {\n"
            "  static ThemeData light() {\n"
            "    return ThemeData(\n"
            "      colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),\n"
            "      useMaterial3: true,\n"
            "    );\n"
            "  }\n"
            "}\n"
        )
        (self.templates_dir / "state_management" / "bloc" / "lib").mkdir(parents=True)
        (self.templates_dir / "state_management" / "bloc" / "lib" / "bloc.dart").write_text(
            "class {{ProjectName}}Bloc {}"
        )
        (self.templates_dir / "core" / "di" / "core" / "di").mkdir(parents=True)
        (
            self.templates_dir / "core" / "di" / "core" / "di" / "feature_registrations.dart"
        ).write_text(
            "import 'package:get_it/get_it.dart';\n\n"
            "Future<void> registerFeatureDependencies(GetIt serviceLocator) async {}\n"
        )
        (self.templates_dir / "core" / "foundation" / "core" / "constants").mkdir(parents=True)
        (
            self.templates_dir / "core" / "foundation" / "core" / "constants" / "app_constants.dart"
        ).write_text(
            "class AppConstants {\n  static const String appName = '{{ProjectName}}';\n}\n"
        )
        (self.templates_dir / "core" / "network_dio" / "core" / "network").mkdir(parents=True)
        (
            self.templates_dir / "core" / "network_dio" / "core" / "network" / "api_client.dart"
        ).write_text("class ApiClient {}\n")
        (self.templates_dir / "navigation" / "go_router" / "app" / "router").mkdir(parents=True)
        (
            self.templates_dir / "navigation" / "go_router" / "app" / "router" / "app_router.dart"
        ).write_text("class AppRouter {}")

        self.output_dir.mkdir(parents=True)

        # Create config
        self.config = Config()
        self.config.set("project_name", "test_app")
        self.config.set("org_id", "com.example")
        self.config.set("state_management", "bloc")
        self.config.set("output_dir", str(self.output_dir))
        self.config.set("include_examples", False)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_initialization(self):
        """Test ProjectGenerator initialization."""
        generator = ProjectGenerator(self.config, self.templates_dir)

        self.assertEqual(generator.config, self.config)
        self.assertEqual(generator.templates_dir, self.templates_dir)
        self.assertIsNone(generator.project_path)

    @patch("fwen.generator.run_command")
    def test_create_flutter_project_success(self, mock_run_command):
        """Test successful Flutter project creation."""
        mock_run_command.return_value = (True, "Flutter project created", "")

        generator = ProjectGenerator(self.config, self.templates_dir)
        success, message = generator._create_flutter_project()

        self.assertTrue(success)
        self.assertIn("created", message.lower())

    @patch("fwen.generator.run_command")
    def test_create_flutter_project_failure(self, mock_run_command):
        """Test failed Flutter project creation."""
        mock_run_command.return_value = (False, "", "Error creating project")

        generator = ProjectGenerator(self.config, self.templates_dir)
        success, message = generator._create_flutter_project()

        self.assertFalse(success)
        self.assertIn("Error", message)

    @patch("fwen.generator.run_command")
    def test_generate_calls_flutter_create(self, mock_run_command):
        """Test that generate() calls flutter create with correct arguments."""
        mock_run_command.return_value = (True, "Success", "")

        # Mock other methods to avoid actual file operations
        with patch.object(ProjectGenerator, "_apply_templates", return_value=(True, "")):
            with patch.object(ProjectGenerator, "_update_pubspec", return_value=(True, "")):
                generator = ProjectGenerator(self.config, self.templates_dir)
                success, message = generator.generate()

        # Verify flutter create was called
        mock_run_command.assert_called_once()
        args = mock_run_command.call_args[0][0]
        self.assertIn("flutter", args)
        self.assertIn("create", args)
        self.assertIn("--org", args)
        self.assertIn("com.example", args)

    @patch.object(
        ProjectGenerator, "_create_flutter_project", return_value=(False, "flutter failed")
    )
    def test_generate_returns_flutter_failure_before_setting_project_path(self, mock_create):
        """generate() should stop immediately when flutter project creation fails."""
        generator = ProjectGenerator(self.config, self.templates_dir)

        success, message = generator.generate()

        self.assertFalse(success)
        self.assertEqual(message, "flutter failed")
        self.assertIsNone(generator.project_path)

    @patch.object(
        ProjectGenerator, "_create_flutter_project", return_value=(False, "flutter failed")
    )
    def test_generate_creates_missing_output_directory(self, mock_create):
        """generate() should create the output directory before invoking flutter."""
        missing_output_dir = Path(self.test_dir) / "missing-output"
        self.config.set("output_dir", str(missing_output_dir))
        generator = ProjectGenerator(self.config, self.templates_dir)

        success, message = generator.generate()

        self.assertFalse(success)
        self.assertEqual(message, "flutter failed")
        self.assertTrue(missing_output_dir.exists())

    @patch.object(ProjectGenerator, "_create_flutter_project", return_value=(True, "ok"))
    @patch.object(ProjectGenerator, "_apply_templates", return_value=(False, "templates failed"))
    def test_generate_returns_template_failure(self, mock_apply, mock_create):
        """generate() should stop when template application fails."""
        generator = ProjectGenerator(self.config, self.templates_dir)

        success, message = generator.generate()

        self.assertFalse(success)
        self.assertEqual(message, "templates failed")
        self.assertEqual(generator.project_path, self.output_dir / "test_app")

    @patch.object(ProjectGenerator, "_create_flutter_project", return_value=(True, "ok"))
    @patch.object(ProjectGenerator, "_apply_templates", return_value=(True, "ok"))
    @patch.object(ProjectGenerator, "_update_pubspec", return_value=(False, "pubspec failed"))
    def test_generate_returns_pubspec_failure(self, mock_pubspec, mock_apply, mock_create):
        """generate() should stop when pubspec updates fail."""
        generator = ProjectGenerator(self.config, self.templates_dir)

        success, message = generator.generate()

        self.assertFalse(success)
        self.assertEqual(message, "pubspec failed")

    @patch.object(ProjectGenerator, "_create_flutter_project", return_value=(True, "ok"))
    @patch.object(ProjectGenerator, "_apply_templates", return_value=(True, "ok"))
    @patch.object(ProjectGenerator, "_update_pubspec", return_value=(True, "ok"))
    @patch.object(
        ProjectGenerator, "_create_initial_feature", return_value=(False, "feature failed")
    )
    def test_generate_returns_feature_failure(
        self, mock_feature, mock_pubspec, mock_apply, mock_create
    ):
        """generate() should stop when the optional initial feature fails."""
        self.config.set("create_feature", True)
        generator = ProjectGenerator(self.config, self.templates_dir)

        success, message = generator.generate()

        self.assertFalse(success)
        self.assertEqual(message, "feature failed")

    @patch("fwen.generator.copy_directory")
    @patch("fwen.generator.run_command")
    def test_apply_templates_copies_base_templates(self, mock_run_command, mock_copy):
        """Test that base templates are copied."""
        mock_run_command.return_value = (True, "", "")
        mock_copy.return_value = None

        # Create a fake project directory
        project_dir = self.output_dir / "test_app"
        project_dir.mkdir(parents=True)
        (project_dir / "lib").mkdir()

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, _ = generator._apply_templates()

        self.assertTrue(success)
        # Verify base templates were copied
        self.assertTrue(mock_copy.called)

    def test_apply_templates_copies_nested_base_app_shell(self):
        """The base app shell chain should be copied with substitutions."""
        project_dir = self.output_dir / "test_app"
        project_dir.mkdir(parents=True)
        (project_dir / "lib").mkdir()

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, _ = generator._apply_templates()

        self.assertTrue(success)
        expected_files = [
            project_dir / "lib" / "app" / "app.dart",
            project_dir / "lib" / "app" / "routes.dart",
            project_dir / "lib" / "app" / "pages" / "home_page.dart",
            project_dir / "lib" / "core" / "di" / "service_locator.dart",
            project_dir / "lib" / "core" / "state_management" / "app_state.dart",
            project_dir / "lib" / "shared" / "themes" / "app_theme.dart",
        ]
        for expected_file in expected_files:
            self.assertTrue(expected_file.exists(), f"Missing copied file: {expected_file}")

        home_page_content = (project_dir / "lib" / "app" / "pages" / "home_page.dart").read_text()
        self.assertIn("TestApp", home_page_content)
        self.assertIn("AppStateScope.of(context)", home_page_content)

    @patch("fwen.generator.copy_directory")
    @patch("fwen.generator.run_command")
    def test_apply_templates_copies_state_management(self, mock_run_command, mock_copy):
        """Test that state management templates are copied."""
        mock_run_command.return_value = (True, "", "")
        mock_copy.return_value = None

        # Create a fake project directory
        project_dir = self.output_dir / "test_app"
        project_dir.mkdir(parents=True)
        (project_dir / "lib").mkdir()

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, message = generator._apply_templates()

        self.assertTrue(success)
        copied_sources = [call.args[0] for call in mock_copy.call_args_list]
        self.assertIn(self.templates_dir / "state_management" / "bloc", copied_sources)
        self.assertIn(self.templates_dir / "navigation" / "go_router", copied_sources)

    def test_apply_templates_without_project_path_fails(self):
        """Applying templates without a project path should fail."""
        generator = ProjectGenerator(self.config, self.templates_dir)

        success, message = generator._apply_templates()

        self.assertFalse(success)
        self.assertEqual(message, "Project path not set")

    @patch("fwen.generator.shutil.rmtree")
    @patch("fwen.generator.copy_directory")
    def test_apply_templates_removes_existing_lib_directory(self, mock_copy, mock_rmtree):
        """Existing lib directories should be removed before applying templates."""
        project_dir = self.output_dir / "test_app"
        (project_dir / "lib").mkdir(parents=True)

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, _ = generator._apply_templates()

        self.assertTrue(success)
        mock_rmtree.assert_called_once_with(project_dir / "lib")

    @patch("fwen.generator.copy_directory")
    def test_apply_templates_copies_navigation_firebase_and_testing_assets(self, mock_copy):
        """Optional navigation, firebase, and testing templates should be applied when present."""
        project_dir = self.output_dir / "test_app"
        (project_dir / "lib").mkdir(parents=True)
        (self.templates_dir / "firebase" / "auth").mkdir(parents=True)
        (self.templates_dir / "testing").mkdir(parents=True)
        self.config.set("include_firebase", True)
        self.config.set("firebase_services", ["auth", "missing"])
        self.config.set("include_testing", True)

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, _ = generator._apply_templates()

        self.assertTrue(success)
        destinations = [call.args[1] for call in mock_copy.call_args_list]
        self.assertIn(project_dir, destinations)
        self.assertIn(project_dir / "lib", destinations)

    def test_apply_templates_missing_implemented_template_fails(self):
        """Missing implemented templates should fail generation."""
        project_dir = self.output_dir / "test_app"
        (project_dir / "lib").mkdir(parents=True)
        shutil.rmtree(self.templates_dir / "navigation" / "go_router")

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, message = generator._apply_templates()

        self.assertFalse(success)
        self.assertIn("navigation.go_router", message)

    @patch("fwen.generator.copy_directory")
    def test_apply_templates_missing_extension_template_is_skipped(self, mock_copy):
        """Missing extension templates should be skipped without errors."""
        project_dir = self.output_dir / "test_app"
        (project_dir / "lib").mkdir(parents=True)
        self.config.set("include_auth", True)

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, message = generator._apply_templates()

        self.assertTrue(success)
        copied_sources = [call.args[0] for call in mock_copy.call_args_list]
        self.assertNotIn(self.templates_dir / "auth", copied_sources)

    @patch("fwen.generator.copy_directory")
    def test_apply_templates_copies_common_feature_infra_templates(self, mock_copy):
        """Common auth, api, persistence, and analytics templates should be applied when present."""
        project_dir = self.output_dir / "test_app"
        (project_dir / "lib").mkdir(parents=True)

        for template_name in ["auth", "api", "persistence", "analytics"]:
            (self.templates_dir / template_name / "lib").mkdir(parents=True)

        self.config.set("include_auth", True)
        self.config.set("include_api", True)
        self.config.set("api_choice", "dio")
        self.config.set("include_persistence", True)
        self.config.set("persistence_choice", "shared_preferences")
        self.config.set("include_analytics", True)
        self.config.set("analytics_choice", "sentry")

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, _ = generator._apply_templates()

        self.assertTrue(success)
        copied_sources = [call.args[0] for call in mock_copy.call_args_list]
        self.assertIn(self.templates_dir / "auth", copied_sources)
        self.assertIn(self.templates_dir / "api", copied_sources)
        self.assertIn(self.templates_dir / "persistence", copied_sources)
        self.assertIn(self.templates_dir / "analytics", copied_sources)
        self.assertIn(self.templates_dir / "core" / "network_dio", copied_sources)

    def test_apply_templates_copies_commerce_reference_when_examples_enabled(self):
        """Commerce reference templates should be copied when include_examples is enabled."""
        project_dir = self.output_dir / "test_app"
        (project_dir / "lib").mkdir(parents=True)
        scenario_root = self.templates_dir / "scenarios" / "commerce_reference" / "lib"
        (scenario_root / "features" / "auth" / "presentation" / "pages").mkdir(parents=True)
        (
            scenario_root / "features" / "auth" / "presentation" / "pages" / "auth_page.dart"
        ).write_text("class AuthPage {}")

        self.config.set("include_examples", True)

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, _ = generator._apply_templates()

        self.assertTrue(success)
        self.assertTrue(
            (
                project_dir
                / "lib"
                / "features"
                / "auth"
                / "presentation"
                / "pages"
                / "auth_page.dart"
            ).exists()
        )

    @patch("fwen.generator.merge_pubspec_dependencies")
    def test_update_pubspec_success(self, mock_merge):
        """Test successful pubspec update."""
        mock_merge.return_value = None

        # Create a fake project with pubspec.yaml
        project_dir = self.output_dir / "test_app"
        project_dir.mkdir(parents=True)
        (project_dir / "pubspec.yaml").write_text("name: test_app\n")

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, message = generator._update_pubspec()

        self.assertTrue(success)
        mock_merge.assert_called_once()

    @patch("fwen.generator.merge_pubspec_dependencies")
    def test_update_pubspec_no_file(self, mock_merge):
        """Test pubspec update when file doesn't exist."""
        # Create project without pubspec.yaml
        project_dir = self.output_dir / "test_app"
        project_dir.mkdir(parents=True)

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = project_dir

        success, message = generator._update_pubspec()

        self.assertFalse(success)
        self.assertIn("not found", message)

    def test_update_pubspec_without_project_path_fails(self):
        """Updating pubspec without a project path should fail."""
        generator = ProjectGenerator(self.config, self.templates_dir)

        success, message = generator._update_pubspec()

        self.assertFalse(success)
        self.assertEqual(message, "Project path not set")

    def test_create_initial_feature_without_project_path_fails(self):
        """Feature creation requires a project path."""
        generator = ProjectGenerator(self.config, self.templates_dir)

        success, message = generator._create_initial_feature()

        self.assertFalse(success)
        self.assertEqual(message, "Project path not set")

    def test_create_initial_feature_without_name_is_noop(self):
        """Missing feature names should be treated as a no-op."""
        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = self.output_dir / "test_app"

        success, message = generator._create_initial_feature()

        self.assertTrue(success)
        self.assertEqual(message, "No feature to create")

    def test_create_initial_feature_missing_script_fails(self):
        """Feature creation should fail when the helper script is unavailable."""
        self.config.set("feature_name", "Auth")
        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = self.output_dir / "test_app"

        success, message = generator._create_initial_feature()

        self.assertFalse(success)
        self.assertEqual(message, "feature-dev.py script not found")

    @patch("fwen.generator.run_command", return_value=(True, "", ""))
    def test_create_initial_feature_success(self, mock_run_command):
        """Feature creation should run the helper script when present."""
        self.config.set("feature_name", "Auth")
        feature_script = Path(self.test_dir) / "scripts" / "feature-dev.py"
        feature_script.parent.mkdir(parents=True)
        feature_script.write_text("print('ok')\n")

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = self.output_dir / "test_app"

        success, message = generator._create_initial_feature()

        self.assertTrue(success)
        self.assertEqual(message, "Feature 'Auth' created")
        mock_run_command.assert_called_once_with(
            ["python3", str(feature_script), "Auth"],
            cwd=str(generator.project_path),
        )

    @patch("fwen.generator.run_command", return_value=(False, "", "script failed"))
    def test_create_initial_feature_failure(self, mock_run_command):
        """Feature creation should surface stderr when the helper script fails."""
        self.config.set("feature_name", "Auth")
        feature_script = Path(self.test_dir) / "scripts" / "feature-dev.py"
        feature_script.parent.mkdir(parents=True)
        feature_script.write_text("print('ok')\n")

        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = self.output_dir / "test_app"

        success, message = generator._create_initial_feature()

        self.assertFalse(success)
        self.assertEqual(message, "Failed to create feature: script failed")

    def test_get_project_path_before_generation(self):
        """Test getting project path before generation."""
        generator = ProjectGenerator(self.config, self.templates_dir)

        path = generator.get_project_path()
        self.assertEqual(path, Path())

    def test_get_project_path_after_generation(self):
        """Test getting project path after setting."""
        generator = ProjectGenerator(self.config, self.templates_dir)
        generator.project_path = self.output_dir / "test_app"

        path = generator.get_project_path()
        self.assertEqual(path, self.output_dir / "test_app")


class TestGenerateProject(unittest.TestCase):
    """Test cases for generate_project module function."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.templates_dir = Path(self.test_dir) / "templates"
        self.output_dir = Path(self.test_dir) / "output"

        # Create minimal template structure
        self.templates_dir.mkdir(parents=True)
        (self.templates_dir / "base" / "lib").mkdir(parents=True)
        self.output_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    @patch("fwen.generator.run_command")
    @patch("fwen.generator.ProjectGenerator._apply_templates")
    @patch("fwen.generator.ProjectGenerator._update_pubspec")
    def test_generate_project_success(self, mock_pubspec, mock_templates, mock_run):
        """Test successful project generation."""
        mock_run.return_value = (True, "", "")
        mock_templates.return_value = (True, "")
        mock_pubspec.return_value = (True, "")

        config = Config()
        config.set("project_name", "test_app")
        config.set("org_id", "com.example")
        config.set("output_dir", str(self.output_dir))

        success, message, path = generate_project(config, self.templates_dir)

        self.assertTrue(success)
        self.assertIsInstance(path, Path)

    @patch("fwen.generator.run_command")
    def test_generate_project_flutter_failure(self, mock_run):
        """Test project generation when Flutter create fails."""
        mock_run.return_value = (False, "", "Flutter error")

        config = Config()
        config.set("project_name", "test_app")
        config.set("org_id", "com.example")
        config.set("output_dir", str(self.output_dir))

        success, message, path = generate_project(config, self.templates_dir)

        self.assertFalse(success)
        self.assertEqual(path, Path())


if __name__ == "__main__":
    unittest.main()
