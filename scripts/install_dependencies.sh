#!/bin/bash

# 核心依赖列表
CORE_DEPENDENCIES=(
  flutter_localizations
  dio
  provider
  intl
  go_router
  url_launcher
  shared_preferences
  connectivity_plus
  flutter_easyloading
  permission_handler
  flutter_svg
  equatable
  get_it
  json_annotation
  freezed_annotation
  logger
  path
  path_provider
  collection
  meta
  rxdart
)

# 开发依赖列表
DEV_DEPENDENCIES=(
  build_runner
  json_serializable
  freezed
  flutter_gen_runner
  intl_utils
  mocktail
)

echo "📦 Installing core dependencies..."
flutter pub add "${CORE_DEPENDENCIES[@]}"

echo "🛠️  Installing dev dependencies..."
flutter pub add --dev "${DEV_DEPENDENCIES[@]}"

echo "✅ Dependencies installed successfully!"
