import 'package:flutter/material.dart';

import '../core/di/service_locator.dart';
import '../core/state_management/app_state.dart';
import '../shared/themes/app_theme.dart';
import 'routes.dart';

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    final controller = appStateController;

    return AppStateScope(
      controller: controller,
      child: AnimatedBuilder(
        animation: controller,
        builder: (context, _) {
          return MaterialApp(
            title: '{{ProjectName}}',
            theme: AppTheme.light(),
            darkTheme: AppTheme.dark(),
            themeMode: controller.state.themeMode,
            initialRoute: AppRoutes.home,
            routes: AppRoutes.routes,
          );
        },
      ),
    );
  }
}
