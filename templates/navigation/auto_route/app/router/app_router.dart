import 'package:auto_route/auto_route.dart';
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
  final routeEntries = configuration.routes.entries.toList();
  final routeDefs = <NamedRouteDef>[
    for (var index = 0; index < routeEntries.length; index += 1)
      NamedRouteDef(
        name: _buildRouteName(routeEntries[index].key, index),
        path: routeEntries[index].key,
        builder: (context, data) => routeEntries[index].value(context),
      ),
  ];

  final appRouter = RootStackRouter.build(
    routes: routeDefs.isEmpty
        ? [
            NamedRouteDef(
              name: 'RootRoute0',
              path: configuration.initialRoute,
              builder: (context, data) => const SizedBox.shrink(),
            ),
          ]
        : routeDefs,
  );

  return MaterialApp.router(
    title: configuration.title,
    theme: configuration.theme,
    darkTheme: configuration.darkTheme,
    themeMode: configuration.themeMode,
    routerConfig: appRouter.config(),
  );
}

String _buildRouteName(String routePath, int index) {
  final words = routePath
      .replaceAll(RegExp(r'[^a-zA-Z0-9]+'), ' ')
      .split(' ')
      .where((word) => word.isNotEmpty)
      .toList();
  final prefix = words.isEmpty
      ? 'Root'
      : words
          .map((word) => '${word[0].toUpperCase()}${word.substring(1)}')
          .join();
  return '${prefix}Route$index';
}
