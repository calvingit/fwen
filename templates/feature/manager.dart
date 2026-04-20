import '../../domain/entities/{{feature_name}}_entity.dart';
import '../../domain/usecases/get_{{feature_name}}_usecase.dart';

class {{FeatureName}}Manager {
  const {{FeatureName}}Manager(this._get{{FeatureName}}UseCase);

  final Get{{FeatureName}}UseCase _get{{FeatureName}}UseCase;

  Future<List<{{FeatureName}}Entity>> load() {
    return _get{{FeatureName}}UseCase();
  }
}
