# Flutter Architecture Guide

This document describes the architecture that `fwen` scaffolds, the directory structure the
generated Flutter app should follow, and the boundaries between layers and feature slices.

## Goals

- Keep domain code independent from Flutter and third-party frameworks.
- Make each feature slice easy to understand, test, and replace.
- Keep architecture decisions understandable without reading template files.

## Architecture Principles

`fwen` follows the standard Clean Architecture dependency rule:

`presentation -> domain <- data`

In practice:

- Presentation depends on domain abstractions and use cases.
- Domain contains entities, repository contracts, and use cases.
- Data implements domain contracts and talks to APIs, local storage, or platform services.
- Shared infrastructure lives in `core/` and `shared/`, but should stay framework-light.

### Layer Responsibilities

| Layer | Responsibility | Notes |
| --- | --- | --- |
| `presentation/` | Widgets, pages, state management adapters | UI should not know about data sources directly. |
| `domain/` | Entities, use cases, repository contracts | Keep this layer pure Dart when possible. |
| `data/` | Repository implementations, models, data sources | Map external data into domain models here. |
| `core/` | Cross-cutting infrastructure | DI, networking, logging, error handling, etc. |
| `shared/` | Reusable UI and app-wide models | Only share things that genuinely repeat across features. |

## Recommended Directory Structure

The project root should stay close to the generated output below. Some folders are always
present, while others are added only when the corresponding CLI option is enabled.

```text
project_root/
├── android/
├── ios/
├── web/
├── macos/
├── windows/
├── linux/
├── lib/
├── test/
├── integration_test/
├── assets/
├── l10n/
├── pubspec.yaml
├── analysis_options.yaml
├── README.md
└── .gitignore
```

### Root-Level Guidelines

- Keep platform folders only for the targets Flutter actually initializes.
- Keep `pubspec.yaml` and analyzer config at the root because they define app-wide behavior.
- Place shared assets at the root, not inside a feature, when multiple features depend on them.
- Keep generated code out of versioned hand-written source unless a package requires committed
  output.

### `lib/` Structure

`lib/` should contain the runtime application code only.

| Directory tree | Purpose |
| --- | --- |
| `lib/` | Runtime application code only. Keep platform-specific or generated assets outside this tree unless they are part of the app runtime. |
| `├── main.dart` | Tiny executable entry point. It should delegate startup and never hold application composition logic. |
| `├── bootstrap.dart` | Startup wrapper that initializes Flutter bindings and launches the root app widget. |
| `├── app/` | App-wide composition root for theme, router, localization, and root shell wiring. |
| `│   ├── app.dart` | Root app widget. Build `MaterialApp` or the equivalent top-level shell here. |
| `│   ├── config/` | Application-wide configuration objects, environment wiring, and root-level flags. |
| `│   │   ├── app_config.dart` | Strongly typed app configuration and bootstrap configuration. |
| `│   │   └── env/` | Environment-specific values such as dev, staging, and production settings. |
| `│   └── router/` | Top-level routing composition for the chosen navigation strategy. |
| `│       ├── app_router.dart` | Root router or route map used by the application shell. |
| `│       └── route_names.dart` | Central route name constants when the router strategy needs them. |
| `├── core/` | Technical infrastructure shared by many features, such as DI, network, storage, analytics, and services. |
| `│   ├── di/` | Dependency injection container setup and registration modules. |
| `│   │   ├── injector.dart` | Root dependency graph composition and service locator entry point. |
| `│   │   └── registrations.dart` | Grouped registrations for services, repositories, and adapters. |
| `│   ├── network/` | HTTP clients, interceptors, API endpoint definitions, and request/response plumbing. |
| `│   │   ├── api_client.dart` | Shared network client wrapper or abstraction. |
| `│   │   ├── api_endpoint.dart` | Endpoint constants or API path definitions. |
| `│   │   └── interceptors/` | Client interceptors, auth headers, retry logic, and request logging. |
| `│   ├── storage/` | Local persistence, secure storage, and cache abstractions. |
| `│   ├── analytics/` | Analytics facades and event-tracking helpers. |
| `│   ├── firebase/` | App-wide Firebase service wrappers and initialization helpers. |
| `│   ├── state_management/` | Shared app-level state containers or global state scaffolds. |
| `│   ├── services/` | Cross-cutting services such as logging, connectivity, device helpers, and runtime utilities. |
| `│   └── usecases/` | App-wide use cases that are not owned by one feature. |
| `├── features/` | Business-capability slices. Each feature may own multiple pages, routes, widgets, and use cases. |
| `│   └── <feature_name>/` | One business capability or user journey, split into data, domain, and presentation layers. |
| `│       ├── data/` | Data sources, models, and repository implementations for the feature. |
| `│       │   ├── datasources/` | Remote APIs, local caches, and third-party adapters for this feature. |
| `│       │   ├── models/` | DTOs and persistence models that map to domain entities. |
| `│       │   └── repositories/` | Concrete repository implementations. |
| `│       ├── domain/` | Pure business logic for the feature. |
| `│       │   ├── entities/` | Feature entities and business objects. |
| `│       │   ├── repositories/` | Repository contracts used by the feature. |
| `│       │   └── usecases/` | Feature actions and orchestration logic. |
| `│       └── presentation/` | UI and state management for this feature. |
| `│           ├── manager/` | Bloc, Cubit, Provider notifier, or Riverpod controller equivalents. |
| `│           ├── pages/` | Screen-level entry points and route destinations. |
| `│           ├── widgets/` | Feature-scoped reusable widgets. |
| `│           └── routes/` | Optional feature-specific route declarations. |
| `├── shared/` | Reusable app-owned presentation code and domain-neutral models that are shared across multiple features. |
| `│   ├── widgets/` | Shared UI primitives, empty states, alert surfaces, and composition widgets. |
| `│   ├── themes/` | Color, spacing, typography, and component theme definitions. |
| `│   ├── models/` | Shared UI models, menu items, filter options, and other cross-feature value objects. |
| `│   └── extensions/` | Stable helper extensions reused by multiple features. |
| `├── generated/` | Optional committed generated output used by packages that require checked-in artifacts. |
| `└── l10n/` | Localization files and generated localizations. |

### `lib/` Guidelines

- `main.dart` should stay tiny and delegate startup to `bootstrap.dart`.
- `bootstrap.dart` should only handle initialization and `runApp`.
- `app/` should contain app-wide composition: theme, router, localization, and top-level shell.
- `core/` should contain technical building blocks that are not tied to one feature.
- `features/` should be organized by business capability, not by layer alone.
- `shared/` should contain reusable code that is genuinely cross-feature.
- `generated/` should only exist if a package requires committed generated output.

### Placement Decision Order

When a class, function, widget, or folder could plausibly fit in more than one place, use this
order:

1. `features/<feature_name>/` if the code belongs to one business capability or user journey.
2. `shared/` if the code is reusable app-owned presentation code or a domain-neutral value model
   that is intentionally shared by multiple features.
3. `core/` if the code is technical infrastructure, SDK integration, or an app-wide service.
4. `app/` if the code composes the whole application shell or root navigation.

If a piece of code still feels ambiguous after this order, ask:

- Does it represent product behavior or technical plumbing?
- Would two unrelated features still need it?
- Could it be replaced without changing user-facing behavior?
- Does it depend on a platform SDK, a network client, or a persistence layer?

These questions usually separate `feature`, `shared`, and `core` cleanly.

### App Shell

The `app/` directory is the composition root for the Flutter application.

```text
lib/app/
├── app.dart
├── config/
└── router/
```

- `app.dart` builds the root `MaterialApp` or equivalent app shell.
- `config/` holds application-wide configuration objects and environment wiring.
- `router/` holds the top-level router or route map for the chosen navigation strategy.

Recommended rule:

- If a file describes the entire app, it belongs in `app/`.
- If a file describes only one feature, it belongs in `features/<feature_name>/`.
- If a file is reusable across features but still app-specific, it belongs in `core/` or `shared/`.

### Core Infrastructure

`core/` collects technical services that many features may depend on.

```text
lib/core/
├── di/
├── network/
├── storage/
├── analytics/
├── firebase/
├── state_management/
├── services/
└── usecases/
```

Recommended contents:

- `di/` for dependency injection setup and registration.
- `network/` for HTTP clients, interceptors, endpoints, and API base configuration.
- `storage/` for local cache, secure storage, and persistence abstractions.
- `analytics/` for analytics facades and event tracking helpers.
- `firebase/` for app-wide Firebase service wrappers.
- `state_management/` for app-level state containers or shared state scaffolds.
- `services/` for cross-cutting services such as logging, connectivity, and device helpers.
- `usecases/` for app-wide use cases that do not belong to one feature.

Core is the right place when the code is:

- an SDK wrapper or integration boundary, such as an HTTP client, Firebase service, or storage
  adapter;
- initialization-heavy and shared across multiple features, such as DI registration or logging;
- technical in nature and not useful as a UI primitive;
- not tied to one business capability.

Core is not the right place when the code is:

- a reusable button, card, empty state, or theme token;
- a feature-specific repository or use case;
- a "common" helper that only exists because it was easy to put somewhere;
- a business rule that just happens to be used in more than one page.

Core layer rules:

- Do not put feature-specific business logic here.
- Prefer abstractions and facades over direct SDK calls.
- Keep dependencies inward-facing: features may use core, but core should not depend on features.

### Feature Slice Pattern

Each feature should be a vertical slice under `lib/features/<feature_name>/`.

Feature boundaries should follow a business capability or user journey, not a single page and not
the router stack itself.

- A feature may have one page or many pages.
- A feature may have one route or a nested route stack.
- A router stack is an implementation detail of presentation; it is not the feature boundary.
- A page is only one screen inside a feature.

Recommended contents:

```text
lib/features/<feature_name>/
├── data/
│   ├── datasources/
│   ├── models/
│   └── repositories/
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── usecases/
└── presentation/
    ├── manager/
    ├── pages/
    ├── widgets/
    └── routes/
```

- `data/datasources/` for remote APIs, local caches, and third-party adapters.
- `data/models/` for DTOs or persistence models that map to domain entities.
- `data/repositories/` for repository implementations.
- `domain/entities/` for business objects and rules that should stay framework-free.
- `domain/repositories/` for repository contracts.
- `domain/usecases/` for application actions and orchestration.
- `presentation/manager/` for Cubit, Bloc, Provider notifier, or Riverpod controller equivalents.
- `presentation/pages/` for screens and route entry pages.
- `presentation/widgets/` for feature-scoped reusable widgets.
- `presentation/routes/` for feature-specific route declarations if needed.

Feature rules:

- The domain layer should never import Flutter.
- Data layer can depend on domain types, but not the other way around.
- Presentation can depend on domain contracts and state managers.
- Keep feature-specific widgets and state close to the feature that owns them.

### Feature Boundary Example

Consider a commerce app:

- `auth` owns sign-in, sign-up, forgot password, and session recovery screens.
- `catalog` owns product browsing, search, product detail, and filters.
- `cart` owns cart items, item quantity changes, and cart summary.
- `checkout` owns address selection, payment, review order, and confirmation.
- `profile` owns account settings, saved addresses, and notification preferences.

The boundary is not "one page = one feature". For example, `catalog` can legitimately contain
multiple pages:

```text
lib/features/catalog/
├── data/
│   ├── datasources/
│   ├── models/
│   └── repositories/
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── usecases/
└── presentation/
    ├── pages/
    │   ├── catalog_page.dart
    │   ├── product_detail_page.dart
    │   └── search_page.dart
    ├── widgets/
    │   ├── product_card.dart
    │   ├── category_chip.dart
    │   └── price_tag.dart
    └── routes/
        └── catalog_routes.dart
```

In this example:

- `catalog_page.dart` is the entry point for the browsing flow.
- `product_detail_page.dart` stays in the same feature because it uses the same product domain,
  repository contracts, and navigation context.
- `search_page.dart` also stays in `catalog` because it still answers the same business question:
  "what should the user discover or inspect?"

Split a feature only when the pages stop sharing the same domain vocabulary, use cases, and data
source expectations. If two pages are just different screens of the same business capability, they
belong in the same feature.

### Shared Code

`shared/` is for reusable app-level code that is not a core infrastructure concern and not a
feature-owned business concept.

```text
lib/shared/
├── widgets/
├── themes/
├── models/
└── extensions/
```

Recommended contents:

- `widgets/` for reusable UI primitives used by more than one feature.
- `themes/` for color schemes, typography, spacing, and component themes.
- `models/` for truly shared UI models or simple app-wide value objects.
- `extensions/` for helper extensions that are widely reused and stable.

Shared exists for code that is reused by multiple features but is still part of the product
experience, not infrastructure. Typical examples include:

- empty states, loading indicators, alert surfaces, and reusable cards;
- buttons, chips, text fields, and other design-system primitives;
- common UI models such as menu items, filter options, or tab descriptors;
- presentation helpers such as label formatters or formatting extensions that are stable and
  app-wide.

Shared layer rules:

- Do not place feature-owned widgets here just because they are reused once.
- If the logic is business-specific, prefer `features/` over `shared/`.
- If the logic is technical and cross-cutting, prefer `core/` over `shared/`.
- If you are only trying to avoid duplication, that alone is not enough reason to move code into
  `shared/`.
- Shared should be small and intentional; if it starts to contain business rules or SDK wrappers,
  it is probably the wrong home.

### Test Structure

Tests should mirror the runtime structure closely.

```text
test/
├── unit/
├── widget/
├── integration/
├── core/
└── features/
    └── <feature_name>/
```

Recommended contents:

- `unit/` for pure Dart tests of entities, use cases, and utilities.
- `widget/` for UI tests of pages and reusable widgets.
- `integration/` for end-to-end app flows.
- `core/` for tests of shared infrastructure.
- `features/<feature_name>/` for feature-scoped test suites.

### Optional Generated Outputs

Some packages or CLI choices can add extra directories:

- `assets/` for image, icon, font, and JSON assets.
- `integration_test/` when integration tests are enabled.
- `generated/` when committed generated code is part of the chosen workflow.
- `l10n/` when localization is enabled.

### Why this structure works

- `app/` contains app-wide bootstrapping and routing.
- `core/` collects reusable technical infrastructure that should not belong to one feature.
- `features/` is split by business capability, not by technical type.
- `shared/` is reserved for truly shared widgets, themes, and models.
- `test/` mirrors runtime code so test ownership stays obvious.
- `l10n/` stays separate so localization does not leak into feature logic.

## Feature Slice Pattern

Each feature should be generated as a vertical slice:

- `domain/entities` defines the business object.
- `domain/repositories` defines the contract.
- `domain/usecases` defines application logic.
- `data/models` maps API or storage payloads into domain objects.
- `data/repositories` implements the contract.
- `presentation/pages` renders the UI.
