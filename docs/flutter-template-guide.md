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

| Template ID | Layer | CLI Dependencies | Source Path | Output Path | Scenario | Mutually Exclusive With | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `base` | `app` | always | `base` | `.` | App bootstrap, shell, and shared skeleton. | - | `implemented` |
| `feature` | `features` | `--create-feature`, `--feature-name` | `feature` | `lib/features/<feature_name>` | Feature scaffold used by `scripts/feature-dev.py`. | - | `implemented` |
| `core.di.feature_registrations` | `core` | always | `core/di` | `lib` | Feature dependency registration connector for DI. | - | `implemented` |
| `state_management.bloc` | `core` | `--state-management=bloc` | `state_management/bloc` | `lib` | Bloc state-management connector. | `state_management.provider`, `state_management.riverpod` | `implemented` |
| `state_management.provider` | `core` | `--state-management=provider` | `state_management/provider` | `lib` | Provider state-management connector. | `state_management.bloc`, `state_management.riverpod` | `implemented` |
| `state_management.riverpod` | `core` | `--state-management=riverpod` | `state_management/riverpod` | `lib` | Riverpod state-management connector. | `state_management.bloc`, `state_management.provider` | `implemented` |
| `navigation.go_router` | `app` | `--navigation=go_router` | `navigation/go_router` | `lib` | GoRouter root routing integration. | `navigation.auto_route`, `navigation.navigator` | `implemented` |
| `navigation.auto_route` | `app` | `--navigation=auto_route` | `navigation/auto_route` | `lib` | AutoRoute root routing integration. | `navigation.go_router`, `navigation.navigator` | `implemented` |
| `navigation.navigator` | `app` | `--navigation=navigator` | `navigation/navigator` | `lib` | Navigator root routing integration. | `navigation.go_router`, `navigation.auto_route` | `implemented` |
| `auth` | `features` | `--include-auth` | `auth` | `.` | Authentication feature extension point. | - | `extension` |
| `api` | `core` | `--include-api` | `api` | `.` | API client extension point. | - | `extension` |
| `persistence` | `core` | `--include-persistence` | `persistence` | `.` | Local persistence extension point. | - | `extension` |
| `analytics` | `core` | `--include-analytics` | `analytics` | `.` | Analytics extension point. | - | `extension` |
| `testing` | `test` | `--include-testing` | `testing` | `.` | Unit/widget testing starter templates. | - | `implemented` |
| `scenario.commerce_reference` | `features` | `--include-examples` | `scenarios/commerce_reference/lib` | `lib` | Multi-feature sample for `auth/catalog/cart/profile`. | - | `implemented` |
| `firebase.<service>` | `core` | `--include-firebase`, `--firebase-services=<service>` | `firebase/<service>` | `.` | Firebase service extension points (`auth/firestore/functions/analytics/messaging/storage/remote_config/crashlytics`). | - | `extension` |

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
