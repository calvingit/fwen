import 'package:flutter/foundation.dart';

import '../../domain/entities/auth_user.dart';

enum AuthStatus { unauthenticated, authenticated }

class AuthManager extends ChangeNotifier {
  AuthStatus status = AuthStatus.unauthenticated;
  AuthUser? user;
  bool isLoading = false;
  String? errorMessage;

  Future<void> signIn({required String email, required String password}) async {
    isLoading = true;
    errorMessage = null;
    notifyListeners();
    await Future<void>.delayed(const Duration(milliseconds: 600));
    if (email.isEmpty || password.isEmpty) {
      errorMessage = 'Email and password are required.';
      isLoading = false;
      notifyListeners();
      return;
    }
    user = AuthUser(
      id: 'user-001',
      email: email,
      displayName: email.split('@').first,
    );
    status = AuthStatus.authenticated;
    isLoading = false;
    notifyListeners();
  }
}
