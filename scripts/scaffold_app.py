#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import shutil

# Determine the absolute path to the templates directory
# This assumes the script is located at .../skills/flutter-app-creator/scripts/scaffold_app.py
# and templates are at .../skills/flutter-app-creator/templates/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../templates"))

def run_command(command, cwd=None):
    """Run a shell command."""
    try:
        subprocess.check_call(command, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        sys.exit(1)

def create_directory(path):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(path, content):
    """Write content to a file."""
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created file: {path}")

def get_template_content(template_path, **kwargs):
    """Read a template file and format it with the provided arguments."""
    full_path = os.path.join(TEMPLATES_DIR, template_path)
    if not os.path.exists(full_path):
        print(f"Error: Template file not found at {full_path}")
        sys.exit(1)

    with open(full_path, 'r') as f:
        content = f.read()

    if kwargs:
        for key, value in kwargs.items():
            content = content.replace('{' + key + '}', str(value))
    return content

def main():
    parser = argparse.ArgumentParser(description="Scaffold a Flutter app based on guidelines.")
    parser.add_argument("name", help="Name of the Flutter project")
    parser.add_argument("--org", help="Organization identifier (e.g. com.example)", default="com.example")
    parser.add_argument("--description", help="Project description", default="A new Flutter project")
    parser.add_argument("--output", help="Output directory", default=".")

    args = parser.parse_args()

    project_name = args.name
    output_dir = os.path.abspath(args.output)
    project_path = os.path.join(output_dir, project_name)

    print(f"Creating Flutter project '{project_name}' in {output_dir}...")

    # 1. Create Flutter Project
    if not os.path.exists(project_path):
        run_command(f"flutter create --org {args.org} --project-name {project_name} --platforms=android,ios {project_name}", cwd=output_dir)
    else:
        print(f"Directory {project_path} already exists. Skipping 'flutter create'.")

    # 2. Setup Directory Structure
    lib_path = os.path.join(project_path, "lib")

    # Define the structure
    dirs_to_create = [
        "app/config",
        "app/router",
        "core/constants",
        "core/errors",
        "core/utils",
        "core/extensions",
        "core/network",
        "core/network/interceptors",
        "core/services",
        "core/di",
        "core/usecases",
        "features",
        "shared/widgets/common",
        "shared/widgets/dialogs",
        "shared/widgets/layouts",
        "shared/themes",
        "shared/models",
        "shared/services",
        "l10n",
        "gen",
        "test/unit",
        "test/widget",
        "test/integration",
        "test/mocks",
        "test/helpers"
    ]

    for d in dirs_to_create:
        create_directory(os.path.join(lib_path, d))

    # Create assets directories
    assets_dirs = [
        "assets/images/common",
        "assets/images/icons",
        "assets/config",
        "assets/i18n",
        "assets/fonts"
    ]
    for d in assets_dirs:
        create_directory(os.path.join(project_path, d))

    # 3. Create Files from Templates

    # bootstrap.dart
    write_file(
        os.path.join(lib_path, "bootstrap.dart"),
        get_template_content("bootstrap.dart")
    )

    # main.dart
    write_file(
        os.path.join(lib_path, "main.dart"),
        get_template_content("main.dart")
    )

    # app/app.dart
    write_file(
        os.path.join(lib_path, "app/app.dart"),
        get_template_content("app/app.dart", project_name=project_name)
    )

    # core/di/injection.dart
    write_file(
        os.path.join(lib_path, "core/di/injection.dart"),
        get_template_content("core/di/injection.dart")
    )

    # core/usecases/usecase.dart
    write_file(
        os.path.join(lib_path, "core/usecases/usecase.dart"),
        get_template_content("core/usecases/usecase.dart")
    )

    # core/constants/app_constants.dart
    write_file(
        os.path.join(lib_path, "core/constants/app_constants.dart"),
        get_template_content("core/constants/app_constants.dart")
    )

    # core/errors/failures.dart
    write_file(
        os.path.join(lib_path, "core/errors/failures.dart"),
        get_template_content("core/errors/failures.dart")
    )

    # core/errors/exceptions.dart
    write_file(
        os.path.join(lib_path, "core/errors/exceptions.dart"),
        get_template_content("core/errors/exceptions.dart")
    )

    # core/utils/logger.dart
    write_file(
        os.path.join(lib_path, "core/utils/logger.dart"),
        get_template_content("core/utils/logger.dart")
    )

    # core/network/api_client.dart
    write_file(
        os.path.join(lib_path, "core/network/api_client.dart"),
        get_template_content("core/network/api_client.dart")
    )

    # shared/themes/app_colors.dart
    write_file(
        os.path.join(lib_path, "shared/themes/app_colors.dart"),
        get_template_content("shared/themes/app_colors.dart")
    )

    # shared/themes/app_theme.dart
    write_file(
        os.path.join(lib_path, "shared/themes/app_theme.dart"),
        get_template_content("shared/themes/app_theme.dart")
    )

    # Create empty .gitkeep in folders to ensure they are tracked if git init
    for d in dirs_to_create:
        write_file(os.path.join(lib_path, d, ".gitkeep"), "")

    print("\n✅ Project setup complete!")
    print(f"cd {project_path}")
    print("\n⚠️  IMPORTANT: Please install dependencies to match the guidelines:")
    print("You can run the provided helper script:")
    print(f"{os.path.join(SCRIPT_DIR, 'install_dependencies.sh')}")
    print("\nOr manually run:")
    print("flutter pub add dio provider shared_preferences connectivity_plus equatable get_it json_annotation freezed_annotation logger bloc flutter_bloc retrofit")
    print("flutter pub add --dev build_runner json_serializable freezed")
    print("\nThen run:")
    print("flutter run")

if __name__ == "__main__":
    main()
