import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:get_it/get_it.dart';

final appNameProvider = Provider<String>((ref) => '{{ProjectName}}');

Future<void> configureStateManagement(GetIt serviceLocator) async {
  if (!serviceLocator.isRegistered<ProviderContainer>()) {
    serviceLocator
        .registerLazySingleton<ProviderContainer>(ProviderContainer.new);
  }
}
