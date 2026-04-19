#!/usr/bin/env python3
import argparse
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../templates"))
ROUTES_TEMPLATE = "base/lib/app/routes.dart"

def get_template_content(template_path, **kwargs):
    """Read a template file and format it with the provided arguments."""
    full_path = os.path.join(TEMPLATES_DIR, template_path)
    if not os.path.exists(full_path):
        print(f"Error: Template file not found at {full_path}")
        sys.exit(1)

    with open(full_path) as f:
        content = f.read()

    if kwargs:
        for key, value in kwargs.items():
            content = content.replace('{{' + key + '}}', str(value))
    return content

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created file: {path}")

def to_pascal_case(s):
    words = re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?=[A-Z]|$)", s.replace("-", "_"))
    if not words:
        words = [part for part in s.replace("-", "_").split("_") if part]
    return ''.join(word.capitalize() for word in words)

def to_snake_case(s):
    normalized = re.sub(r"[\s-]+", "_", s)
    snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", normalized).lower()
    return re.sub(r"_+", "_", snake_case).strip("_")

def update_routes_file(routes_file_path, feature_name, pascal_name, snake_name):
    if not os.path.exists(routes_file_path):
        # Create from template if not exists
        print(f"Routes file not found at {routes_file_path}. Creating it...")
        content = get_template_content(ROUTES_TEMPLATE)
        write_file(routes_file_path, content)

    with open(routes_file_path) as f:
        content = f.read()

    # 1. Add Import
    import_line = f"import '../features/{snake_name}/presentation/pages/{snake_name}_page.dart';"
    if import_line not in content:
        # Add import after the last import or at the top
        if "import " in content:
            last_import_index = content.rfind("import ")
            end_of_line = content.find("\n", last_import_index) + 1
            content = content[:end_of_line] + import_line + "\n" + content[end_of_line:]
        else:
            content = import_line + "\n" + content
        print(f"Added import to {routes_file_path}")

    # 2. Add Route
    route_entry = f"    {pascal_name}Page.routeName: (context) => const {pascal_name}Page(),"

    if route_entry.strip() in content:
        print(f"Route for {pascal_name} already exists.")
        return

    # Find the routes map
    # Look for 'static final Map<String, WidgetBuilder> routes = {'
    pattern = r"(static final Map<String, WidgetBuilder> routes = \{)"
    match = re.search(pattern, content)

    if match:
        end_pos = match.end()
        content = content[:end_pos] + "\n" + route_entry + content[end_pos:]

        with open(routes_file_path, 'w') as f:
            f.write(content)
        print(f"Updated routes in {routes_file_path}")
    else:
        print(f"Error: Could not find 'routes' map in {routes_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Create a new feature module.")
    parser.add_argument("name", help="Name of the feature (e.g. Login)")

    args = parser.parse_args()

    name = args.name
    pascal_name = to_pascal_case(name)
    snake_name = to_snake_case(name)

    print(f"Creating feature '{pascal_name}'...")

    # Verify we are in a flutter project root (roughly)
    if not os.path.exists("lib"):
        print("Error: 'lib' directory not found. Please run this script from the root of your Flutter project.")
        sys.exit(1)

    # Directories
    base_feature_dir = os.path.join("lib", "features", snake_name)

    # Data Layer
    data_dir = os.path.join(base_feature_dir, "data")
    data_datasources_dir = os.path.join(data_dir, "datasources")
    data_models_dir = os.path.join(data_dir, "models")
    data_repo_dir = os.path.join(data_dir, "repositories")

    # Domain Layer
    domain_dir = os.path.join(base_feature_dir, "domain")
    domain_entities_dir = os.path.join(domain_dir, "entities")
    domain_repo_dir = os.path.join(domain_dir, "repositories")
    domain_usecases_dir = os.path.join(domain_dir, "usecases")

    # Presentation Layer
    presentation_dir = os.path.join(base_feature_dir, "presentation")
    presentation_manager_dir = os.path.join(presentation_dir, "manager")
    presentation_page_dir = os.path.join(presentation_dir, "pages")
    presentation_widgets_dir = os.path.join(presentation_dir, "widgets")

    # Create all directories
    dirs_to_create = [
        data_datasources_dir, data_models_dir, data_repo_dir,
        domain_entities_dir, domain_repo_dir, domain_usecases_dir,
        presentation_manager_dir, presentation_page_dir, presentation_widgets_dir
    ]

    for d in dirs_to_create:
        create_directory(d)

    # Files

    # Domain: Entity
    entity_content = get_template_content("feature/entity.dart", FeatureName=pascal_name)
    entity_path = os.path.join(domain_entities_dir, f"{snake_name}_entity.dart")
    write_file(entity_path, entity_content)

    # Data: Model
    model_content = get_template_content("feature/model.dart", FeatureName=pascal_name, feature_name=snake_name)
    model_path = os.path.join(data_models_dir, f"{snake_name}_model.dart")
    write_file(model_path, model_content)

    # Domain: Repository Interface
    repo_interface_content = get_template_content("feature/repository_interface.dart", FeatureName=pascal_name)
    repo_interface_path = os.path.join(domain_repo_dir, f"{snake_name}_repository.dart")
    write_file(repo_interface_path, repo_interface_content)

    # Domain: UseCase
    usecase_content = get_template_content("feature/usecase.dart", FeatureName=pascal_name, feature_name=snake_name)
    usecase_path = os.path.join(domain_usecases_dir, f"get_{snake_name}_usecase.dart")
    write_file(usecase_path, usecase_content)

    # Data: Repository Implementation
    repo_impl_content = get_template_content("feature/repository_impl.dart", FeatureName=pascal_name, feature_name=snake_name)
    repo_impl_path = os.path.join(data_repo_dir, f"{snake_name}_repository_impl.dart")
    write_file(repo_impl_path, repo_impl_content)

    # Presentation: Page
    page_content = get_template_content("feature/page.dart", FeatureName=pascal_name, feature_name=snake_name)
    page_path = os.path.join(presentation_page_dir, f"{snake_name}_page.dart")
    write_file(page_path, page_content)

    # Routes
    routes_file = os.path.join("lib", "app", "routes.dart")
    update_routes_file(routes_file, name, pascal_name, snake_name)

    print(f"Feature '{pascal_name}' created successfully.")

if __name__ == "__main__":
    main()
