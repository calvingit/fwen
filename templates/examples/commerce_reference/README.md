# Commerce Reference Scenario

`commerce_reference` is a minimal multi-feature template set for `fwen`.
It answers one concrete question: how `auth`, `catalog`, `cart`, and `profile`
are sliced as independent features and run together in one app.

## Purpose

This scenario is a reference for feature boundaries and coexistence:

- each feature keeps its own domain and presentation layer;
- each feature provides its own manager and entry page;
- app-level route wiring stays in one place under `app/routes.dart`.

## Included Template Set

Source templates are under:

`templates/scenarios/commerce_reference/lib/`

It includes:

- `app/routes.dart` to aggregate routes for all feature pages;
- `features/auth/**` with entity, usecase, manager, page;
- `features/catalog/**` with entity, usecase, manager, page;
- `features/cart/**` with entity, usecase, manager, page;
- `features/profile/**` with entity, usecase, manager, page.

## How To Use

Copy this scenario tree into your generated project `lib/` and integrate
with your selected app shell template.

## Placeholder Rules

The templates follow existing placeholder conventions:

- `{{ProjectName}}` for app-facing labels;
- `{{project_name}}` for generated ids and sample data values.

No project name is hardcoded in this scenario.
