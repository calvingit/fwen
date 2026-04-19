import 'package:flutter/material.dart';

Route<dynamic> onGenerateRoute(RouteSettings settings) {
  return MaterialPageRoute<void>(
    builder: (context) => const SizedBox.shrink(),
    settings: settings,
  );
}
