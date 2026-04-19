import 'package:flutter/material.dart';

class {{FeatureName}}Page extends StatelessWidget {
  const {{FeatureName}}Page({super.key});

  static const routeName = '/{{feature_name}}';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('{{FeatureName}}'),
      ),
      body: const Center(
        child: Text('{{FeatureName}} feature'),
      ),
    );
  }
}
