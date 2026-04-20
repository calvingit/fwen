import 'package:flutter/foundation.dart';
import 'package:get_it/get_it.dart';

class AppProviderManager extends ChangeNotifier {
  int counter = 0;

  void increment() {
    counter += 1;
    notifyListeners();
  }
}

Future<void> configureStateManagement(GetIt serviceLocator) async {
  if (!serviceLocator.isRegistered<AppProviderManager>()) {
    serviceLocator
        .registerLazySingleton<AppProviderManager>(AppProviderManager.new);
  }
}
