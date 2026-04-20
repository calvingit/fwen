import 'dart:async';

/// Base interface for all use cases.
///
/// [Type] is the return type.
/// [Params] is the parameter type.
abstract class UseCase<Type, Params> {
  FutureOr<Type> call(Params params);
}

/// Helper class for use cases with no input parameters.
class NoParams {}
