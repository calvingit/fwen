import '../entities/auth_user.dart';

class GetSignedInUserUseCase {
  const GetSignedInUserUseCase();

  Future<AuthUser> call() async {
    return const AuthUser(
      id: '{{project_name}}-auth-user',
      email: 'guest@{{project_name}}.app',
      displayName: 'Guest User',
    );
  }
}
