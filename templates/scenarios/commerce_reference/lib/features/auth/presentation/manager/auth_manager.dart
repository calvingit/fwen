import 'package:flutter/foundation.dart';

import '../../domain/entities/auth_user.dart';
import '../../domain/usecases/get_signed_in_user_usecase.dart';

class AuthManager extends ChangeNotifier {
  AuthManager({GetSignedInUserUseCase? getSignedInUser})
    : _getSignedInUser = getSignedInUser ?? const GetSignedInUserUseCase();

  final GetSignedInUserUseCase _getSignedInUser;

  AuthUser? user;

  Future<void> load() async {
    user = await _getSignedInUser();
    notifyListeners();
  }
}
