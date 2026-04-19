import 'package:flutter/material.dart';

class AppState {
  const AppState({
    this.themeMode = ThemeMode.system,
  });

  final ThemeMode themeMode;

  AppState copyWith({
    ThemeMode? themeMode,
  }) {
    return AppState(
      themeMode: themeMode ?? this.themeMode,
    );
  }
}

class AppStateController extends ChangeNotifier {
  AppStateController([AppState initialState = const AppState()]) : _state = initialState;

  AppState _state;

  AppState get state => _state;

  void setThemeMode(ThemeMode themeMode) {
    if (_state.themeMode == themeMode) {
      return;
    }

    _state = _state.copyWith(themeMode: themeMode);
    notifyListeners();
  }

  void resetThemeMode() {
    setThemeMode(ThemeMode.system);
  }
}

class AppStateScope extends InheritedNotifier<AppStateController> {
  const AppStateScope({
    super.key,
    required AppStateController controller,
    required super.child,
  }) : super(notifier: controller);

  static AppStateController of(BuildContext context) {
    final scope = context.dependOnInheritedWidgetOfExactType<AppStateScope>();
    final controller = scope?.notifier;
    if (controller == null) {
      throw FlutterError('AppStateScope not found in the widget tree.');
    }

    return controller;
  }
}
