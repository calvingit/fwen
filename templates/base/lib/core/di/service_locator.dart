import 'package:get_it/get_it.dart';

import 'feature_registrations.dart';
import '../state_management/app_state.dart';

final GetIt serviceLocator = GetIt.instance;

Future<void> configureDependencies() async {
  if (serviceLocator.isRegistered<AppStateController>()) {
    return;
  }

  serviceLocator.registerSingleton<AppStateController>(AppStateController());
  await registerFeatureDependencies(serviceLocator);
}

AppStateController get appStateController =>
    serviceLocator<AppStateController>();
