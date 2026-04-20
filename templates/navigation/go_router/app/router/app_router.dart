import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

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
  final goRouter = GoRouter(
    initialLocation: configuration.initialRoute,
    routes: configuration.routes.entries
        .map(
          (entry) => GoRoute(
            path: entry.key,
            builder: (context, state) => entry.value(context),
          ),
        )
        .toList(),
  );

  return MaterialApp.router(
    title: configuration.title,
    theme: configuration.theme,
    darkTheme: configuration.darkTheme,
    themeMode: configuration.themeMode,
    routerConfig: goRouter,
  );
}
