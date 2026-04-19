import 'package:flutter/widgets.dart';

import 'app/app.dart';
import 'core/di/service_locator.dart';

Future<void> bootstrap() async {
  WidgetsFlutterBinding.ensureInitialized();
  await configureDependencies();
  runApp(const App());
}
