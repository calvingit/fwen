import 'package:flutter/material.dart';

import 'pages/home_page.dart';

class AppRoutes {
  static const home = '/';

  static final Map<String, WidgetBuilder> routes = {
    home: (context) => const HomePage(),
  };
}
