import '../entities/{{feature_name}}_entity.dart';

abstract class {{FeatureName}}Repository {
  Future<List<{{FeatureName}}Entity>> getAll();
}
