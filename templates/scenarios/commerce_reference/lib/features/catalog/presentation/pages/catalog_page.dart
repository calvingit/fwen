import 'package:flutter/material.dart';

import '../manager/catalog_manager.dart';

class CatalogPage extends StatefulWidget {
  const CatalogPage({super.key});

  static const routeName = '/catalog';

  @override
  State<CatalogPage> createState() => _CatalogPageState();
}

class _CatalogPageState extends State<CatalogPage> {
  late final CatalogManager _manager;

  @override
  void initState() {
    super.initState();
    _manager = CatalogManager();
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
        return Scaffold(
          appBar: AppBar(title: const Text('Catalog')),
          body: ListView.builder(
            itemCount: _manager.items.length,
            itemBuilder: (context, index) {
              final item = _manager.items[index];

              return ListTile(
                title: Text(item.name),
                subtitle: Text('\$${(item.priceCents / 100).toStringAsFixed(2)}'),
              );
            },
          ),
        );
      },
    );
  }
}
