"""
Command-line argument parser for Flutter Clean CLI.
Supports both interactive and non-interactive modes.
"""

import argparse


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with all CLI options."""
    parser = argparse.ArgumentParser(
        prog="fwen",
        description="Create Flutter apps with Clean Architecture from scratch.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (default)
  fwen

  # Non-interactive mode with basic options
  fwen --project-name my_app --org com.example

  # Full non-interactive mode
  fwen \\
    --project-name my_app \\
    --org com.example \\
    --state-management bloc \\
    --navigation go_router \\
    --platforms ios android \\
    --include-api \\
    --api-choice dio
        """,
    )

    # Required arguments
    parser.add_argument(
        "--project-name",
        type=str,
        help="Project name in snake_case (e.g., my_awesome_app)",
    )

    # Basic options
    parser.add_argument(
        "--org",
        type=str,
        default="com.example",
        help="Organization identifier in reverse domain format (default: com.example)",
    )
    parser.add_argument(
        "--description",
        type=str,
        default="A new Flutter project with Clean Architecture",
        help="Project description",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Output directory for the project (default: current directory)",
    )

    # Architecture options
    parser.add_argument(
        "--state-management",
        type=str,
        choices=["bloc", "provider", "riverpod"],
        default="bloc",
        help="State management solution (default: bloc)",
    )
    parser.add_argument(
        "--navigation",
        type=str,
        choices=["go_router", "auto_route", "navigator"],
        default="go_router",
        help="Navigation solution (default: go_router)",
    )
    parser.add_argument(
        "--dependency-injection",
        type=str,
        choices=["get_it", "provider", "riverpod"],
        default="get_it",
        help="Dependency injection solution (default: get_it)",
    )
    parser.add_argument(
        "--no-examples",
        action="store_true",
        help="Don't include example code",
    )

    # Platform options
    parser.add_argument(
        "--platforms",
        type=str,
        nargs="+",
        choices=["ios", "android", "web", "macos", "windows", "linux"],
        default=["ios", "android"],
        help="Target platforms (default: ios android)",
    )

    # Authentication
    parser.add_argument(
        "--include-auth",
        action="store_true",
        help="Include authentication setup",
    )
    parser.add_argument(
        "--auth-methods",
        type=str,
        nargs="+",
        choices=["email", "google", "apple", "phone"],
        help="Authentication methods (requires --include-auth)",
    )

    # Firebase
    parser.add_argument(
        "--include-firebase",
        action="store_true",
        help="Include Firebase setup",
    )
    parser.add_argument(
        "--firebase-services",
        type=str,
        nargs="+",
        choices=[
            "auth",
            "firestore",
            "functions",
            "analytics",
            "messaging",
            "storage",
            "remote_config",
            "crashlytics",
        ],
        help="Firebase services (requires --include-firebase)",
    )

    # Development tools
    parser.add_argument(
        "--include-api",
        action="store_true",
        help="Include API layer setup",
    )
    parser.add_argument(
        "--api-choice",
        type=str,
        choices=["dio", "retrofit", "fetch"],
        help="HTTP client for API (requires --include-api)",
    )

    parser.add_argument(
        "--include-persistence",
        action="store_true",
        help="Include state persistence setup",
    )
    parser.add_argument(
        "--persistence-choice",
        type=str,
        choices=["shared_preferences", "hive", "isar"],
        help="Persistence solution (requires --include-persistence)",
    )

    parser.add_argument(
        "--include-analytics",
        action="store_true",
        help="Include analytics setup",
    )
    parser.add_argument(
        "--analytics-choice",
        type=str,
        choices=["firebase_analytics", "sentry", "mixpanel"],
        help="Analytics service (requires --include-analytics)",
    )

    parser.add_argument(
        "--include-testing",
        action="store_true",
        help="Include testing setup",
    )
    parser.add_argument(
        "--testing-types",
        type=str,
        nargs="+",
        choices=["unit", "widget", "integration"],
        help="Testing types (requires --include-testing)",
    )

    parser.add_argument(
        "--include-ci",
        action="store_true",
        help="Include CI/CD configuration",
    )
    parser.add_argument(
        "--ci-choice",
        type=str,
        choices=["github_actions", "gitlab_ci"],
        help="CI/CD platform (requires --include-ci)",
    )

    # Initial feature
    parser.add_argument(
        "--feature-name",
        type=str,
        help="Create initial feature with this name (PascalCase)",
    )

    # Mode selection
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Force interactive mode even with arguments provided",
    )

    parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Skip confirmation prompt in non-interactive mode",
    )

    return parser


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = create_parser()
    return parser.parse_args(args)


def args_to_config(args: argparse.Namespace) -> dict:
    """Convert parsed arguments to config dictionary."""
    config = {
        # Basic info
        "project_name": args.project_name,
        "org_id": args.org,
        "description": args.description,
        "output_dir": args.output_dir,
        # Architecture
        "state_management": args.state_management,
        "navigation": args.navigation,
        "dependency_injection": args.dependency_injection,
        "include_examples": not args.no_examples,
        # Platforms
        "platforms": args.platforms,
        # Auth
        "include_auth": args.include_auth,
        "auth_methods": args.auth_methods or [],
        # Firebase
        "include_firebase": args.include_firebase,
        "firebase_services": args.firebase_services or [],
        # Development tools
        "include_api": args.include_api,
        "api_choice": args.api_choice,
        "include_persistence": args.include_persistence,
        "persistence_choice": args.persistence_choice,
        "include_analytics": args.include_analytics,
        "analytics_choice": args.analytics_choice,
        "include_testing": args.include_testing,
        "testing_types": args.testing_types or [],
        "include_ci": args.include_ci,
        "ci_choice": args.ci_choice,
        # Initial feature
        "create_feature": args.feature_name is not None,
        "feature_name": args.feature_name,
    }

    # Filter out None values
    return {k: v for k, v in config.items() if v is not None}


def should_use_interactive_mode(args: argparse.Namespace) -> bool:
    """Determine if interactive mode should be used."""
    # Use interactive mode if explicitly requested
    if args.interactive:
        return True

    # Use interactive mode if project_name is not provided
    if not args.project_name:
        return True

    # Otherwise, use non-interactive mode
    return False


def validate_args(args: argparse.Namespace) -> tuple[bool, str | None]:
    """Validate command-line arguments."""
    # Check auth methods
    if args.include_auth and not args.auth_methods:
        return False, "--auth-methods required when --include-auth is set"

    # Check firebase services
    if args.include_firebase and not args.firebase_services:
        return False, "--firebase-services required when --include-firebase is set"

    # Check api choice
    if args.include_api and not args.api_choice:
        return False, "--api-choice required when --include-api is set"

    # Check persistence choice
    if args.include_persistence and not args.persistence_choice:
        return False, "--persistence-choice required when --include-persistence is set"

    # Check analytics choice
    if args.include_analytics and not args.analytics_choice:
        return False, "--analytics-choice required when --include-analytics is set"

    # Check testing types
    if args.include_testing and not args.testing_types:
        return False, "--testing-types required when --include-testing is set"

    # Check ci choice
    if args.include_ci and not args.ci_choice:
        return False, "--ci-choice required when --include-ci is set"

    # Check project name format
    if args.project_name:
        from fwen.config import Config

        config = Config()
        is_valid, error = config.validate_project_name(args.project_name)
        if not is_valid:
            return False, f"Invalid project name: {error}"

    return True, None
