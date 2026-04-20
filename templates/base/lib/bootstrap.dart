import 'package:flutter/widgets.dart';

import 'app/app.dart';
import 'core/di/service_locator.dart';
import 'core/state_management/app_state_management.dart';

Future<void> bootstrap() async {
  WidgetsFlutterBinding.ensureInitialized();
  await configureDependencies();
  await configureStateManagement(serviceLocator);
  runApp(const App());
}
