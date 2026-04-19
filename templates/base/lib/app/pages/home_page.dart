import 'package:flutter/material.dart';

import '../../core/state_management/app_state.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final appStateController = AppStateScope.of(context);
    final appState = appStateController.state;

    return Scaffold(
      appBar: AppBar(
        title: const Text('{{ProjectName}}'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const Text('{{ProjectName}} app shell'),
              const SizedBox(height: 12),
              Text('Theme mode: ${appState.themeMode.name}'),
              const SizedBox(height: 24),
              Wrap(
                spacing: 12,
                runSpacing: 12,
                alignment: WrapAlignment.center,
                children: [
                  FilledButton(
                    onPressed: () {
                      appStateController.setThemeMode(ThemeMode.system);
                    },
                    child: const Text('System'),
                  ),
                  FilledButton.tonal(
                    onPressed: () {
                      appStateController.setThemeMode(ThemeMode.light);
                    },
                    child: const Text('Light'),
                  ),
                  OutlinedButton(
                    onPressed: () {
                      appStateController.setThemeMode(ThemeMode.dark);
                    },
                    child: const Text('Dark'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
