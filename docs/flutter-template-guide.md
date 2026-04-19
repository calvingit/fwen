# Flutter Template Guide

This document is the implementation-facing source of truth for template categories, template
scope, and placement decisions in `fwen`.

It answers two questions:

1. Which template categories exist today, and which ones are extension points.
2. When generated code should land in `app/`, `core/`, `shared/`, or `features/`.

## Template Registry

The registry below groups the template categories that `fwen` recognizes.

Only categories marked as `implemented today` are backed by template files in this repository now.
Categories marked `reference-only / extension point` are documented so the CLI and future template
work can share the same vocabulary, but they are not yet treated as first-class shipped template
families.

| Category | Status | Template root | What it covers | Basis |
| --- | --- | --- | --- | --- |
| `base` | implemented today | `templates/base` | App bootstrap, root app shell, shared theme wiring. | Flutter entry point and app startup contract. |
| `feature` | implemented today | `templates/feature` | Generic feature slice scaffold with data, domain, and presentation layers. | Clean Architecture vertical slice. |
| `testing` | implemented today | `templates/testing` | Starter test files for unit and widget tests. | Flutter testing conventions and smoke-test patterns. |
| `state_management` | reference-only / extension point | `templates/state_management/{bloc,provider,riverpod}` | App-level state management shell. | Public API and idioms of the selected package. |
| `navigation` | reference-only / extension point | `templates/navigation/{go_router,auto_route,navigator}` | Root router bootstrap and top-level navigation wiring. | Public API of the selected routing strategy. |
| `auth` | reference-only / extension point | `templates/auth` | Authentication feature slice starter. | Auth-related business capability. |
| `api` | reference-only / extension point | `templates/api` | Network client and endpoint scaffolds. | API integration boundary. |
| `persistence` | reference-only / extension point | `templates/persistence` | Local storage and cache scaffolds. | Persistence boundary. |
| `analytics` | reference-only / extension point | `templates/analytics` | Analytics facade and event-tracking shell. | Cross-cutting telemetry boundary. |
| `firebase` | reference-only / extension point | `templates/firebase/{service}` | Service-specific Firebase scaffolds. | Firebase service boundaries. |

### Category Intent

- `base` should stay small and predictable. It defines the minimum app runtime skeleton.
- `feature` should generate one business capability or user journey, not a whole app.
- `testing` should create only the starter coverage that helps validate the generated app shape.
- `state_management` and `navigation` are root-level composition choices, not business features.
- `auth`, `api`, `persistence`, `analytics`, and `firebase` are optional expansion points that
  usually plug into `core/`, `shared/`, or `features/` depending on what they generate.

## Template Decision Matrix

Use the matrix below when deciding where a template belongs in the generated project structure.
The template should be placed where the generated code will live, not where the template file
itself happens to sit in this repository.

| If the template generates... | Put it in... | Example output | Do not use this location when... |
| --- | --- | --- | --- |
| App bootstrap, top-level shell, or root route composition | `app/` | `lib/app/app.dart`, `lib/app/router/app_router.dart` | The code is only for one feature. |
| Technical infrastructure, SDK wrappers, or shared app services | `core/` | `lib/core/network/api_client.dart`, `lib/core/storage/local_storage.dart` | The code is a reusable UI primitive or theme token. |
| Reusable app-owned UI, neutral models, or cross-feature presentation helpers | `shared/` | `lib/shared/widgets/...`, `lib/shared/themes/...` | The code is infrastructure or a feature-specific rule. |
| One business capability or user journey | `features/<feature>/` | `lib/features/auth/...`, `lib/features/catalog/...` | The code is only a root shell or global service. |

### Placement Rules

Use these rules in order:

1. If the code composes the whole application, place it in `app/`.
2. If the code is technical infrastructure used by many parts of the app, place it in `core/`.
3. If the code is a reusable app-owned UI or domain-neutral model shared by multiple features,
   place it in `shared/`.
4. If the code belongs to a single business capability, place it in `features/<feature>/`.

### Quick Checks

Ask these questions before choosing a location:

- Does this code describe the app shell or a single feature?
- Is the main value infrastructure, or reuse?
- Would two unrelated features both depend on it?
- Would changing it affect user-facing business behavior, or only app wiring?

Interpretation:

- `app/` is for composition, not business rules.
- `core/` is for plumbing, not shared widgets.
- `shared/` is for reusable product assets, not infrastructure.
- `features/` is for business behavior, even when that behavior is reused across several pages in
  the same feature.

## Current Template Map

The table below lists the shipped template files that exist in the repository today.

| Template file | Generated location | Purpose |
| --- | --- | --- |
| `templates/base/lib/main.dart` | `lib/main.dart` | Tiny executable entry point that calls bootstrap. |
| `templates/base/lib/bootstrap.dart` | `lib/bootstrap.dart` | App startup wrapper and `runApp` entry point. |
| `templates/base/lib/app/app.dart` | `lib/app/app.dart` | Root app widget and shell composition. |
| `templates/base/lib/app/routes.dart` | `lib/app/routes.dart` | Default route map and home route scaffold. |
| `templates/feature/entity.dart` | `lib/features/<feature>/domain/entities/<feature>_entity.dart` | Pure domain entity. |
| `templates/feature/model.dart` | `lib/features/<feature>/data/models/<feature>_model.dart` | Data-layer model mapping to the entity. |
| `templates/feature/repository_interface.dart` | `lib/features/<feature>/domain/repositories/<feature>_repository.dart` | Domain repository contract. |
| `templates/feature/repository_impl.dart` | `lib/features/<feature>/data/repositories/<feature>_repository_impl.dart` | Data-layer repository implementation. |
| `templates/feature/usecase.dart` | `lib/features/<feature>/domain/usecases/get_<feature>_usecase.dart` | Use case that orchestrates feature behavior. |
| `templates/feature/page.dart` | `lib/features/<feature>/presentation/pages/<feature>_page.dart` | Feature presentation entry page. |
| `templates/testing/test/widget/app_smoke_test.dart` | `test/widget/app_smoke_test.dart` | Widget smoke-test starter. |
| `templates/testing/test/unit/app_state_test.dart` | `test/unit/app_state_test.dart` | Unit-test starter. |

## Template Contract

Every template should obey the same rules:

- Use `{{variable}}` placeholders only.
- Keep names aligned with `Config.get_substitution_vars()`.
- Do not hard-code project-specific values that already exist in config.
- Prefer minimal code that compiles cleanly and demonstrates the intended pattern.
- Avoid coupling a template to a different architecture choice unless that template is explicitly
  responsible for that choice.

The current substitution variables are:

- `{{project_name}}`
- `{{ProjectName}}`
- `{{projectName}}`
- `{{org_id}}`
- `{{description}}`
- `{{state_management}}`
- `{{navigation}}`

## Extension Point Guidance

The following categories are intentionally treated as extension points until their shipped template
files are expanded further:

- `state_management`
- `navigation`
- `auth`
- `api`
- `persistence`
- `analytics`
- `firebase`

That means:

- the template doc should describe what they are allowed to generate, but not pretend they are
  fully fleshed-out product templates;
- any future template files in those categories should keep the same placement rules above;
- each new template should be documented before or together with its implementation.

## Adding New Templates

When you add a new template category, document these items first:

1. Which generated location it targets.
2. Which package or official pattern it is based on.
3. Which files it creates.
4. Which config flags control it.
5. Which placeholders it uses.
6. Whether it can coexist with the existing architecture options.

If a template cannot answer those six questions clearly, it is probably too vague to add.
