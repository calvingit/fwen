import '../entities/{{feature_name}}_entity.dart';
import '../repositories/{{feature_name}}_repository.dart';

class Get{{FeatureName}}UseCase {
  const Get{{FeatureName}}UseCase(this.repository);

  final {{FeatureName}}Repository repository;

  Future<List<{{FeatureName}}Entity>> call() {
    return repository.getAll();
  }
}
