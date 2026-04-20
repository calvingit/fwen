import 'package:get_it/get_it.dart';

/// Global service locator instance.
final GetIt getIt = GetIt.instance;

/// Initializes application dependencies.
///
/// Projects can extend this method with concrete registrations.
Future<void> init() async {
  await Future<void>.value();
}
