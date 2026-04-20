import 'package:flutter/material.dart';

import '../manager/auth_manager.dart';

class AuthPage extends StatefulWidget {
  const AuthPage({super.key});

  static const routeName = '/auth';

  @override
  State<AuthPage> createState() => _AuthPageState();
}

class _AuthPageState extends State<AuthPage> {
  late final AuthManager _manager;

  @override
  void initState() {
    super.initState();
    _manager = AuthManager();
    _manager.load();
  }

  @override
  void dispose() {
    _manager.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _manager,
      builder: (context, _) {
        final user = _manager.user;

        return Scaffold(
          appBar: AppBar(title: const Text('Auth')),
          body: Center(
            child: user == null
                ? const CircularProgressIndicator()
                : Text(
                    'Welcome ${user.displayName}\n{{ProjectName}} auth entry',
                    textAlign: TextAlign.center,
                  ),
          ),
        );
      },
    );
  }
}
