# Commerce Reference Scenario

This directory is a concrete multi-feature Flutter app reference for `fwen`.

It is intentionally small, but it shows the structural decisions that matter in a real app:

- how multiple feature slices coexist in one app;
- how one feature can own multiple pages and nested routes;
- how `shared` widgets differ from feature-owned widgets;
- how `core` stays focused on app-wide technical infrastructure instead of generic dumping ground code.

## What This Scenario Represents

The app is a commerce-style product experience with these feature slices:

- `auth` for sign-in and entry flow;
- `catalog` for browsing, category drill-down, and product details;
- `cart` for basket management;
- `checkout` for the order placement flow;
- `profile` for account-related actions.

The key architectural rule is that each feature owns its own presentation and business logic. Shared UI primitives live in `lib/shared`, while app-wide infrastructure lives in `lib/core`.

## Structure Overview

```text
lib/
├── app/
│   ├── app.dart
│   ├── pages/
│   │   └── home_page.dart
│   └── router/
│       ├── app_router.dart
│       └── app_routes.dart
├── core/
│   ├── di/
│   │   └── injector.dart
│   └── network/
│       └── api_client.dart
├── features/
│   ├── auth/
│   ├── catalog/
│   ├── cart/
│   ├── checkout/
│   └── profile/
└── shared/
    └── widgets/
```

## Why This Scenario Exists

This reference is meant to answer the questions that usually slow teams down when they first adopt
Clean Architecture:

1. Where does a feature start and end?
2. When should a page become a feature slice instead of just another widget?
3. Which widgets are safe to share across features?
4. What belongs in `core` versus `shared` versus a feature folder?

## Shared vs Feature-Owned Widgets

Use `shared` for product-level primitives that are reused across features:

- section headers;
- empty states;
- entry cards used by the app shell;
- other neutral UI building blocks with no business meaning.

Keep feature-owned widgets inside the feature that uses them:

- `catalog` product cards;
- `cart` item rows;
- `profile` menu tiles;
- any widget that encodes feature-specific language or behavior.

## Core Boundary

Keep `core` for app-wide technical infrastructure:

- dependency injection;
- network clients;
- persistence abstractions;
- global analytics;
- bootstrap-level services.

If a file is only "common" because it seems reusable, that is not enough to put it in `core`.
It should belong to `shared` if it is UI-like, or stay inside the owning feature if it is tied to
feature behavior.

## Feature Ownership Example

The `catalog` feature intentionally includes multiple pages and nested route ownership:

- `catalog_page.dart` for the browsing entry point;
- `category_page.dart` for category drill-down;
- `product_details_page.dart` for product inspection;
- `catalog_router.dart` for the feature-local route map;
- `product_card.dart` as a widget only catalog uses.

This is the pattern the rest of the app follows.

