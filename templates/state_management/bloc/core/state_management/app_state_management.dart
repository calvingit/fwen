import 'package:bloc/bloc.dart';
import 'package:get_it/get_it.dart';

class AppBlocManager extends Cubit<int> {
  AppBlocManager() : super(0);
}

class AppBlocLoggingObserver extends BlocObserver {}

Future<void> configureStateManagement(GetIt serviceLocator) async {
  if (Bloc.observer is! AppBlocLoggingObserver) {
    Bloc.observer = AppBlocLoggingObserver();
  }

  if (!serviceLocator.isRegistered<AppBlocManager>()) {
    serviceLocator.registerLazySingleton<AppBlocManager>(AppBlocManager.new);
  }
}
