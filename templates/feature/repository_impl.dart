import '../../domain/entities/{{feature_name}}_entity.dart';
import '../../domain/repositories/{{feature_name}}_repository.dart';

class {{FeatureName}}RepositoryImpl implements {{FeatureName}}Repository {
  const {{FeatureName}}RepositoryImpl();

  @override
  Future<List<{{FeatureName}}Entity>> getAll() async {
    return const [];
  }
}
