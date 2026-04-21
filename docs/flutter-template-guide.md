# Flutter Template Guide

`fwen` uses a single template fact source: [`src/fwen/template_registry.py`](../src/fwen/template_registry.py).

- The generator (`src/fwen/generator.py`) selects and copies templates from this registry.
- Repository asset tests validate template existence from this registry.
- This document mirrors the same registry contract and decision rules.

## Registry Contract

Each registry entry (`TemplateRegistration`) defines:

| Field | Meaning |
| --- | --- |
| `template_id` | Unique template key used across docs/tests/generator. |
| `layer` | Ownership layer in generated project (`app/core/shared/features/test`). |
| `cli_dependencies` | CLI switches that must be set for this template to apply. |
| `source_path` | Source directory under `templates/`. |
| `output_path` | Target directory under generated project root. |
| `scenario` | Intended use case boundary for this template. |
| `mutually_exclusive_with` | Other template IDs that cannot coexist in one run. |
| `status` | `implemented` or `extension`. |

### Status Semantics

- `implemented`: required when selected. Missing template path causes generator failure.
- `extension`: optional when selected. Missing template path is skipped.

## Template Registry Snapshot

The table below reflects the current registry entries.

<!-- TEMPLATE_REGISTRY_TABLE:START -->

| Template ID | Layer | CLI Dependencies | Source Path | Output Path | Scenario | Mutually Exclusive With | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `base` | `app` | always | `base` | `.` | App bootstrap, shell wiring, and shared app skeleton. | - | `implemented` |
| `feature` | `features` | --create-feature, --feature-name | `feature` | `lib/features/<feature_name>` | Feature vertical-slice scaffold used by scripts/feature-dev.py. | - | `implemented` |
| `core.di.feature_registrations` | `core` | always | `core/di` | `lib` | Core DI extension point for feature-level registrations. | - | `implemented` |
| `core.foundation` | `core` | always | `core/foundation` | `lib` | Shared core primitives: constants, failures, usecases, logger, and theme colors. | - | `implemented` |
| `state_management.bloc` | `core` | --state-management=bloc | `state_management/bloc` | `lib` | State-management connector for bloc projects. | state_management.provider, state_management.riverpod | `implemented` |
| `state_management.provider` | `core` | --state-management=provider | `state_management/provider` | `lib` | State-management connector for provider projects. | state_management.bloc, state_management.riverpod | `implemented` |
| `state_management.riverpod` | `core` | --state-management=riverpod | `state_management/riverpod` | `lib` | State-management connector for riverpod projects. | state_management.bloc, state_management.provider | `implemented` |
| `navigation.go_router` | `app` | --navigation=go_router | `navigation/go_router` | `lib` | Root router integration for go_router. | navigation.auto_route, navigation.navigator | `implemented` |
| `navigation.auto_route` | `app` | --navigation=auto_route | `navigation/auto_route` | `lib` | Root router integration for auto_route. | navigation.go_router, navigation.navigator | `implemented` |
| `navigation.navigator` | `app` | --navigation=navigator | `navigation/navigator` | `lib` | Root router integration for Navigator 2.0. | navigation.go_router, navigation.auto_route | `implemented` |
| `auth` | `features` | --include-auth | `auth` | `.` | Email authentication feature: domain entities, repository, usecases, data layer, and login page. | - | `implemented` |
| `api` | `core` | --include-api | `api` | `.` | Network API extension point. | - | `extension` |
| `core.network_api.dio` | `core` | --include-api, --api-choice=dio | `core/network_dio` | `lib` | Dio-based API client scaffold for network integration. | - | `implemented` |
| `core.network_api.retrofit` | `core` | --include-api, --api-choice=retrofit | `core/network_dio` | `lib` | Dio API client scaffold reused by retrofit integration. | - | `implemented` |
| `persistence` | `core` | --include-persistence | `persistence` | `.` | StorageService abstract interface + SharedPreferences implementation. | - | `implemented` |
| `analytics` | `core` | --include-analytics | `analytics` | `.` | AnalyticsService abstract interface + Firebase Analytics, Sentry, and Mixpanel implementations. | - | `implemented` |
| `testing` | `test` | --include-testing | `testing` | `.` | Starter unit/widget testing templates. | - | `implemented` |
| `scenario.commerce_reference` | `features` | --include-examples | `scenarios/commerce_reference/lib` | `lib` | Multi-feature reference scenario for auth/catalog/cart/profile. | - | `implemented` |
| `firebase.auth` | `core` | --include-firebase, --firebase-services=auth | `firebase/auth` | `.` | Firebase auth extension point. | - | `extension` |
| `firebase.firestore` | `core` | --include-firebase, --firebase-services=firestore | `firebase/firestore` | `.` | Firebase firestore extension point. | - | `extension` |
| `firebase.functions` | `core` | --include-firebase, --firebase-services=functions | `firebase/functions` | `.` | Firebase functions extension point. | - | `extension` |
| `firebase.analytics` | `core` | --include-firebase, --firebase-services=analytics | `firebase/analytics` | `.` | Firebase analytics extension point. | - | `extension` |
| `firebase.messaging` | `core` | --include-firebase, --firebase-services=messaging | `firebase/messaging` | `.` | Firebase messaging extension point. | - | `extension` |
| `firebase.storage` | `core` | --include-firebase, --firebase-services=storage | `firebase/storage` | `.` | Firebase storage extension point. | - | `extension` |
| `firebase.remote_config` | `core` | --include-firebase, --firebase-services=remote_config | `firebase/remote_config` | `.` | Firebase remote_config extension point. | - | `extension` |
| `firebase.crashlytics` | `core` | --include-firebase, --firebase-services=crashlytics | `firebase/crashlytics` | `.` | Firebase crashlytics extension point. | - | `extension` |

<!-- TEMPLATE_REGISTRY_TABLE:END -->

## Template Decision Matrix

This matrix defines where a new template belongs.

| Decision Question | Target Layer | Typical Output |
| --- | --- | --- |
| App-level assembly, startup, root router wiring? | `app` | `lib/app/**`, `lib/bootstrap.dart` |
| Technical infrastructure shared by many features? | `core` | `lib/core/**` |
| Reusable product UI or domain-neutral shared artifacts? | `shared` | `lib/shared/**` |
| Business capability owned by one domain area? | `features` | `lib/features/<feature>/**` |
| Test-only scaffolding? | `test` | `test/**` |

Use this check order when adding templates:

1. Determine ownership layer from the matrix above.
2. Register a new `template_id` in `template_registry.py`.
3. Define CLI dependencies, source path, output path, scenario, and mutual exclusivity.
4. Set `status` to `implemented` only when the template directory is shipped in repo.
5. Keep generator behavior aligned by using the registry entry only.

## Generator Behavior

`ProjectGenerator._apply_templates()` follows this flow:

1. Remove generated `lib/` from `flutter create`.
2. Read selected templates from `iter_selected_templates(config)`.
3. Copy each template from `templates/<source_path>` into `<project>/<output_path>`.
4. On missing template directory:
   - `implemented` -> fail fast with explicit error.
   - `extension` -> skip silently and continue.

This keeps documentation, test expectations, and runtime generation behavior aligned through one
registry definition.
