import 'package:flutter/material.dart';

import '../../../../app/routes.dart';
import '../manager/auth_manager.dart';

class AuthPage extends StatefulWidget {
  const AuthPage({super.key});

  static const routeName = '/auth';

  @override
  State<AuthPage> createState() => _AuthPageState();
}

class _AuthPageState extends State<AuthPage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  late final AuthManager _manager;

  @override
  void initState() {
    super.initState();
    _manager = AuthManager();
  }

  @override
  void dispose() {
    _manager.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _signIn() async {
    await _manager.signIn(
      email: _emailController.text.trim(),
      password: _passwordController.text,
    );
    if (_manager.status == AuthStatus.authenticated && mounted) {
      Navigator.of(context).pushReplacementNamed(AppRoutes.shell);
    }
  }

  void _continueAsGuest() {
    Navigator.of(context).pushReplacementNamed(AppRoutes.shell);
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _manager,
      builder: (context, _) {
        return Scaffold(
          appBar: AppBar(title: const Text('{{ProjectName}}')),
          body: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 400),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    const Icon(Icons.storefront, size: 72, color: Colors.blueGrey),
                    const SizedBox(height: 24),
                    TextField(
                      controller: _emailController,
                      decoration: const InputDecoration(
                        labelText: 'Email',
                        border: OutlineInputBorder(),
                      ),
                      keyboardType: TextInputType.emailAddress,
                    ),
                    const SizedBox(height: 12),
                    TextField(
                      controller: _passwordController,
                      decoration: const InputDecoration(
                        labelText: 'Password',
                        border: OutlineInputBorder(),
                      ),
                      obscureText: true,
                    ),
                    if (_manager.errorMessage != null) ...[
                      const SizedBox(height: 8),
                      Text(
                        _manager.errorMessage!,
                        style: TextStyle(color: Theme.of(context).colorScheme.error),
                      ),
                    ],
                    const SizedBox(height: 16),
                    FilledButton(
                      onPressed: _manager.isLoading ? null : _signIn,
                      child: _manager.isLoading
                          ? const SizedBox(
                              height: 20,
                              width: 20,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                          : const Text('Sign In'),
                    ),
                    const SizedBox(height: 8),
                    OutlinedButton(
                      onPressed: _continueAsGuest,
                      child: const Text('Continue as Guest'),
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}
