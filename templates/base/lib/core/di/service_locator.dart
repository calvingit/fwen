import 'package:get_it/get_it.dart';

import '../state_management/app_state.dart';

final GetIt serviceLocator = GetIt.instance;

Future<void> configureDependencies() async {
  if (!serviceLocator.isRegistered<AppStateController>()) {
    serviceLocator.registerSingleton<AppStateController>(
      AppStateController(),
    );
  }
}

AppStateController get appStateController => serviceLocator<AppStateController>();
