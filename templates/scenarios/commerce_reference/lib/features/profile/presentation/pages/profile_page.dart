import 'package:flutter/material.dart';

import '../manager/profile_manager.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  static const routeName = '/profile';

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  late final ProfileManager _manager;

  @override
  void initState() {
    super.initState();
    _manager = ProfileManager();
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
        final summary = _manager.summary;

        return Scaffold(
          appBar: AppBar(title: const Text('Profile')),
          body: Center(
            child: summary == null
                ? const CircularProgressIndicator()
                : Text(
                    '${summary.name}\n${summary.email}\nMember since ${summary.memberSince}',
                    textAlign: TextAlign.center,
                  ),
          ),
        );
      },
    );
  }
}
