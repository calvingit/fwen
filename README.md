# fwen

> Flutter Clean Architecture scaffolder - Create production-ready Flutter apps with Clean Architecture in seconds.

[![PyPI](https://img.shields.io/pypi/v/fwen)](https://pypi.org/project/fwen/)
[![Python](https://img.shields.io/pypi/pyversions/fwen)](https://pypi.org/project/fwen/)
[![License](https://img.shields.io/github/license/calvingit/fwen)](LICENSE)
[![Tests](https://img.shields.io/github/actions/workflow/status/calvingit/fwen/test.yml)](https://github.com/calvingit/fwen/actions)

---

## Table of Contents

- [Overview](#overview)
- [Why fwen?](#why-fwen)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Overview

**fwen** is a command-line tool that scaffolds Flutter applications following Clean Architecture principles. It generates a complete project structure with configurable state management, navigation, dependency injection, and optional integrations for Firebase, authentication, analytics, testing, and CI/CD.

## Why fwen?

- 🏗️ **Clean Architecture** - Pre-configured layer separation (core, features, shared)
- ⚡ **Fast** - Create a full project in seconds with interactive or non-interactive CLI
- 🔧 **Configurable** - Support for Bloc, Provider, Riverpod, GoRouter, AutoRoute, and more
- 📦 **Batteries Included** - Optional Firebase, authentication, persistence, analytics setup
- 🧪 **Testing Ready** - Generated projects include testing structure
- 🚀 **Production-Ready** - Bootstrap error handling, logging, and best practices

## Features

### Architecture Options
- **State Management**: Bloc, Provider, Riverpod
- **Navigation**: GoRouter, AutoRoute, Navigator 2.0
- **Dependency Injection**: GetIt, Provider, Riverpod

### Integrations
- **Firebase**: Auth, Firestore, Functions, Analytics, Messaging, Storage
- **Authentication**: Email, Google, Apple, Phone
- **API Layer**: Dio, Retrofit
- **Persistence**: Shared Preferences, Hive, Isar
- **Analytics**: Firebase Analytics, Sentry, Mixpanel
- **CI/CD**: GitHub Actions, GitLab CI

### Platform Support
- iOS, Android, Web, macOS, Windows, Linux

## Installation

### Prerequisites
- Python 3.11+
- Flutter 3.22.0+
- Dart 3.4.0+

### Using uv (Recommended)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install fwen
uv pip install fwen

# Or run directly with uv
uvx fwen --project-name my_app
```

### Using pip

```bash
pip install fwen
```

### From Source

```bash
git clone https://github.com/calvingit/fwen.git
cd fwen
uv pip install -e .
```

## Quick Start

### Interactive Mode

Run without arguments for step-by-step prompts:

```bash
fwen
```

### Non-Interactive Mode

Pass all options via command-line arguments:

```bash
# Basic usage
fwen --project-name my_app --org com.example

# Full example with all options
fwen \
  --project-name my_awesome_app \
  --org com.mycompany \
  --description "My Awesome App" \
  --state-management bloc \
  --navigation go_router \
  --platforms ios android web \
  --include-api \
  --api-choice dio \
  --yes
```

### Generated Project Structure

```
lib/
├── bootstrap.dart              # App initialization & error handling
├── main.dart                   # Entry point
├── app/                        # App configuration & router
│   ├── config/
│   └── router/
├── core/                       # Core infrastructure
│   ├── di/
│   ├── network/
│   ├── services/
│   ├── blocs/                  # State management (if Bloc)
│   └── usecases/
├── features/                   # Feature modules
├── shared/                     # Shared UI & entities
│   ├── widgets/
│   ├── themes/
│   └── models/
├── l10n/                       # Localization
└── gen/                        # Generated code
```

## Documentation

### Command-Line Arguments

**Required:**
- `--project-name` - Project name in snake_case

**Basic Options:**
- `--org` - Organization ID (default: com.example)
- `--description` - Project description
- `--output-dir` - Output directory (default: current)

**Architecture:**
- `--state-management` - bloc|provider|riverpod (default: bloc)
- `--navigation` - go_router|auto_route|navigator (default: go_router)
- `--dependency-injection` - get_it|provider|riverpod (default: get_it)
- `--no-examples` - Skip example code

**Platforms:**
- `--platforms` - ios android web macos windows linux (default: ios android)

**Features:**
- `--include-auth` -- `--auth-methods` email google apple phone
- `--include-firebase` -- `--firebase-services` auth firestore analytics messaging storage
- `--include-api` -- `--api-choice` dio retrofit fetch
- `--include-persistence` -- `--persistence-choice` shared_preferences hive isar
- `--include-analytics` -- `--analytics-choice` firebase_analytics sentry mixpanel
- `--include-testing` -- `--testing-types` unit widget integration
- `--include-ci` -- `--ci-choice` github_actions gitlab_ci

**Other:**
- `--feature-name` - Create initial feature
- `--yes, -y` - Skip confirmation
- `--interactive, -i` - Force interactive mode

### Feature Generator

Use the feature generator script to add new features:

```bash
fwen-feature <FeatureName>
```

Example:

```bash
fwen-feature Auth
```

**Creates:**
- `lib/features/auth/data/repositories/auth_repository.dart`
- `lib/features/auth/presentation/pages/auth_page.dart`
- Updates `lib/app/routes.dart` with new route

### Available Options

| Category | Options |
|----------|---------|
| State Management | Bloc, Provider, Riverpod |
| Navigation | GoRouter, AutoRoute, Navigator 2.0 |
| DI | GetIt, Provider, Riverpod |
| Platforms | iOS, Android, Web, macOS, Windows, Linux |
| API | Dio, Retrofit, Fetch |
| Persistence | Shared Preferences, Hive, Isar |
| Analytics | Firebase Analytics, Sentry, Mixpanel |
| CI/CD | GitHub Actions, GitLab CI |

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT © calvingit

---

**Made with ❤️ by the Flutter community**
