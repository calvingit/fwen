import 'package:flutter/material.dart';

import '../features/auth/presentation/pages/auth_page.dart';
import 'shell_page.dart';

class AppRoutes {
  static const auth = '/auth';
  static const shell = '/shell';

  static const initialRoute = auth;
  static const appTitle = '{{ProjectName}} Commerce Reference';

  static final Map<String, WidgetBuilder> routes = {
    auth: (context) => const AuthPage(),
    shell: (context) => const ShellPage(),
  };
}
