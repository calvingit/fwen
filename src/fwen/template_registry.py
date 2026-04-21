"""Template registry definitions shared by docs, tests, and generator."""

from dataclasses import dataclass
from typing import Any, Literal

from .config import Config

TemplateStatus = Literal["implemented", "extension"]
MatchMode = Literal["equals", "contains"]


@dataclass(frozen=True)
class ConfigRequirement:
    """A config requirement used to activate a template registration."""

    key: str
    expected: Any
    match_mode: MatchMode = "equals"

    def matches(self, config: Config) -> bool:
        """Return whether the requirement matches the current config."""
        actual = config.get(self.key)
        if self.match_mode == "equals":
            return actual == self.expected
        if self.match_mode == "contains":
            if isinstance(actual, (list, tuple, set)):
                return self.expected in actual
            return False
        raise ValueError(f"Unsupported match_mode: {self.match_mode}")


@dataclass(frozen=True)
class TemplateRegistration:
    """Template registry entry consumed by generator and documentation."""

    template_id: str
    layer: str
    cli_dependencies: tuple[str, ...]
    source_path: str
    output_path: str
    scenario: str
    mutually_exclusive_with: tuple[str, ...]
    status: TemplateStatus
    config_requirements: tuple[ConfigRequirement, ...] = ()
    applies_during_generation: bool = True


def _build_registry() -> tuple[TemplateRegistration, ...]:
    """Build the full template registry."""
    entries: list[TemplateRegistration] = [
        TemplateRegistration(
            template_id="base",
            layer="app",
            cli_dependencies=(),
            source_path="base",
            output_path=".",
            scenario="App bootstrap, shell wiring, and shared app skeleton.",
            mutually_exclusive_with=(),
            status="implemented",
        ),
        TemplateRegistration(
            template_id="feature",
            layer="features",
            cli_dependencies=("--create-feature", "--feature-name"),
            source_path="feature",
            output_path="lib/features/<feature_name>",
            scenario="Feature vertical-slice scaffold used by scripts/feature-dev.py.",
            mutually_exclusive_with=(),
            status="implemented",
            applies_during_generation=False,
        ),
        TemplateRegistration(
            template_id="core.di.feature_registrations",
            layer="core",
            cli_dependencies=(),
            source_path="core/di",
            output_path="lib",
            scenario="Core DI extension point for feature-level registrations.",
            mutually_exclusive_with=(),
            status="implemented",
        ),
        TemplateRegistration(
            template_id="core.foundation",
            layer="core",
            cli_dependencies=(),
            source_path="core/foundation",
            output_path="lib",
            scenario="Shared core primitives: constants, failures, usecases, logger, and theme colors.",
            mutually_exclusive_with=(),
            status="implemented",
        ),
        TemplateRegistration(
            template_id="state_management.bloc",
            layer="core",
            cli_dependencies=("--state-management=bloc",),
            source_path="state_management/bloc",
            output_path="lib",
            scenario="State-management connector for bloc projects.",
            mutually_exclusive_with=(
                "state_management.provider",
                "state_management.riverpod",
            ),
            status="implemented",
            config_requirements=(ConfigRequirement("state_management", "bloc"),),
        ),
        TemplateRegistration(
            template_id="state_management.provider",
            layer="core",
            cli_dependencies=("--state-management=provider",),
            source_path="state_management/provider",
            output_path="lib",
            scenario="State-management connector for provider projects.",
            mutually_exclusive_with=(
                "state_management.bloc",
                "state_management.riverpod",
            ),
            status="implemented",
            config_requirements=(ConfigRequirement("state_management", "provider"),),
        ),
        TemplateRegistration(
            template_id="state_management.riverpod",
            layer="core",
            cli_dependencies=("--state-management=riverpod",),
            source_path="state_management/riverpod",
            output_path="lib",
            scenario="State-management connector for riverpod projects.",
            mutually_exclusive_with=(
                "state_management.bloc",
                "state_management.provider",
            ),
            status="implemented",
            config_requirements=(ConfigRequirement("state_management", "riverpod"),),
        ),
        TemplateRegistration(
            template_id="navigation.go_router",
            layer="app",
            cli_dependencies=("--navigation=go_router",),
            source_path="navigation/go_router",
            output_path="lib",
            scenario="Root router integration for go_router.",
            mutually_exclusive_with=(
                "navigation.auto_route",
                "navigation.navigator",
            ),
            status="implemented",
            config_requirements=(ConfigRequirement("navigation", "go_router"),),
        ),
        TemplateRegistration(
            template_id="navigation.auto_route",
            layer="app",
            cli_dependencies=("--navigation=auto_route",),
            source_path="navigation/auto_route",
            output_path="lib",
            scenario="Root router integration for auto_route.",
            mutually_exclusive_with=(
                "navigation.go_router",
                "navigation.navigator",
            ),
            status="implemented",
            config_requirements=(ConfigRequirement("navigation", "auto_route"),),
        ),
        TemplateRegistration(
            template_id="navigation.navigator",
            layer="app",
            cli_dependencies=("--navigation=navigator",),
            source_path="navigation/navigator",
            output_path="lib",
            scenario="Root router integration for Navigator 2.0.",
            mutually_exclusive_with=(
                "navigation.go_router",
                "navigation.auto_route",
            ),
            status="implemented",
            config_requirements=(ConfigRequirement("navigation", "navigator"),),
        ),
        TemplateRegistration(
            template_id="auth",
            layer="features",
            cli_dependencies=("--include-auth",),
            source_path="auth",
            output_path=".",
            scenario="Email authentication feature: domain entities, repository, usecases, data layer, and login page.",
            mutually_exclusive_with=(),
            status="implemented",
            config_requirements=(ConfigRequirement("include_auth", True),),
        ),
        TemplateRegistration(
            template_id="api",
            layer="core",
            cli_dependencies=("--include-api",),
            source_path="api",
            output_path=".",
            scenario="Network API extension point.",
            mutually_exclusive_with=(),
            status="extension",
            config_requirements=(ConfigRequirement("include_api", True),),
        ),
        TemplateRegistration(
            template_id="core.network_api.dio",
            layer="core",
            cli_dependencies=("--include-api", "--api-choice=dio"),
            source_path="core/network_dio",
            output_path="lib",
            scenario="Dio-based API client scaffold for network integration.",
            mutually_exclusive_with=(),
            status="implemented",
            config_requirements=(
                ConfigRequirement("include_api", True),
                ConfigRequirement("api_choice", "dio"),
            ),
        ),
        TemplateRegistration(
            template_id="core.network_api.retrofit",
            layer="core",
            cli_dependencies=("--include-api", "--api-choice=retrofit"),
            source_path="core/network_dio",
            output_path="lib",
            scenario="Dio API client scaffold reused by retrofit integration.",
            mutually_exclusive_with=(),
            status="implemented",
            config_requirements=(
                ConfigRequirement("include_api", True),
                ConfigRequirement("api_choice", "retrofit"),
            ),
        ),
        TemplateRegistration(
            template_id="persistence",
            layer="core",
            cli_dependencies=("--include-persistence",),
            source_path="persistence",
            output_path=".",
            scenario="StorageService abstract interface + SharedPreferences implementation.",
            mutually_exclusive_with=(),
            status="implemented",
            config_requirements=(ConfigRequirement("include_persistence", True),),
        ),
        TemplateRegistration(
            template_id="analytics",
            layer="core",
            cli_dependencies=("--include-analytics",),
            source_path="analytics",
            output_path=".",
            scenario="AnalyticsService abstract interface + Firebase Analytics, Sentry, and Mixpanel implementations.",
            mutually_exclusive_with=(),
            status="implemented",
            config_requirements=(ConfigRequirement("include_analytics", True),),
        ),
        TemplateRegistration(
            template_id="testing",
            layer="test",
            cli_dependencies=("--include-testing",),
            source_path="testing",
            output_path=".",
            scenario="Starter unit/widget testing templates.",
            mutually_exclusive_with=(),
            status="implemented",
            config_requirements=(ConfigRequirement("include_testing", True),),
        ),
        TemplateRegistration(
            template_id="scenario.commerce_reference",
            layer="features",
            cli_dependencies=("--include-examples",),
            source_path="scenarios/commerce_reference/lib",
            output_path="lib",
            scenario="Multi-feature reference scenario for auth/catalog/cart/profile.",
            mutually_exclusive_with=(),
            status="implemented",
            config_requirements=(ConfigRequirement("include_examples", True),),
        ),
    ]

    for service in Config.FIREBASE_SERVICES:
        entries.append(
            TemplateRegistration(
                template_id=f"firebase.{service}",
                layer="core",
                cli_dependencies=("--include-firebase", f"--firebase-services={service}"),
                source_path=f"firebase/{service}",
                output_path=".",
                scenario=f"Firebase {service} extension point.",
                mutually_exclusive_with=(),
                status="extension",
                config_requirements=(
                    ConfigRequirement("include_firebase", True),
                    ConfigRequirement("firebase_services", service, "contains"),
                ),
            )
        )

    return tuple(entries)


TEMPLATE_REGISTRY = _build_registry()


def get_template_registry() -> tuple[TemplateRegistration, ...]:
    """Return the immutable template registry."""
    return TEMPLATE_REGISTRY


def get_implemented_templates() -> tuple[TemplateRegistration, ...]:
    """Return templates that must exist in the repository."""
    return tuple(template for template in TEMPLATE_REGISTRY if template.status == "implemented")


def iter_selected_templates(config: Config) -> tuple[TemplateRegistration, ...]:
    """Return templates selected by the current config for project generation."""
    selected: list[TemplateRegistration] = []
    for template in TEMPLATE_REGISTRY:
        if not template.applies_during_generation:
            continue
        if all(requirement.matches(config) for requirement in template.config_requirements):
            selected.append(template)
    return tuple(selected)
