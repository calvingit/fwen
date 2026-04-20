import 'package:flutter/material.dart';

class AppRouterConfiguration {
  const AppRouterConfiguration({
    required this.title,
    required this.theme,
    required this.darkTheme,
    required this.themeMode,
    required this.initialRoute,
    required this.routes,
  });

  final String title;
  final ThemeData theme;
  final ThemeData darkTheme;
  final ThemeMode themeMode;
  final String initialRoute;
  final Map<String, WidgetBuilder> routes;
}

Widget buildAppRouter(AppRouterConfiguration configuration) {
  return MaterialApp(
    title: configuration.title,
    theme: configuration.theme,
    darkTheme: configuration.darkTheme,
    themeMode: configuration.themeMode,
    initialRoute: configuration.initialRoute,
    onGenerateRoute: (settings) => _onGenerateRoute(settings, configuration),
  );
}

Route<dynamic> _onGenerateRoute(
  RouteSettings settings,
  AppRouterConfiguration configuration,
) {
  final routeBuilder = configuration.routes[settings.name];
  if (routeBuilder != null) {
    return MaterialPageRoute<void>(
      builder: routeBuilder,
      settings: settings,
    );
  }

  final fallbackBuilder = configuration.routes[configuration.initialRoute] ??
      (configuration.routes.values.isEmpty
          ? null
          : configuration.routes.values.first);

  return MaterialPageRoute<void>(
    builder: fallbackBuilder ?? (_) => const SizedBox.shrink(),
    settings: settings,
  );
}
