import 'package:flutter/material.dart';

import '../../../../features/cart/domain/cart_state.dart';
import '../manager/catalog_manager.dart';

class CatalogPage extends StatefulWidget {
  const CatalogPage({super.key, required this.cartState});

  final CartState cartState;

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

  String _formatPrice(int cents) => '\$${(cents / 100).toStringAsFixed(2)}';

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _manager,
      builder: (context, _) {
        return Scaffold(
          appBar: AppBar(title: const Text('{{ProjectName}} Catalog')),
          body: _manager.isLoading
              ? const Center(child: CircularProgressIndicator())
              : _manager.error != null
                  ? Center(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(Icons.error_outline, size: 48, color: Colors.red),
                          const SizedBox(height: 8),
                          Text(_manager.error!),
                          TextButton(
                              onPressed: _manager.load, child: const Text('Retry')),
                        ],
                      ),
                    )
                  : AnimatedBuilder(
                      animation: widget.cartState,
                      builder: (context, _) {
                        return ListView.builder(
                          padding: const EdgeInsets.symmetric(vertical: 8),
                          itemCount: _manager.items.length,
                          itemBuilder: (context, index) {
                            final item = _manager.items[index];
                            final inCart = widget.cartState.items
                                .any((c) => c.sku == item.id);
                            return Card(
                              margin: const EdgeInsets.symmetric(
                                  horizontal: 16, vertical: 4),
                              child: ListTile(
                                leading: CircleAvatar(
                                  child: Text('${index + 1}'),
                                ),
                                title: Text(item.name),
                                subtitle: Text(_formatPrice(item.priceCents)),
                                trailing: FilledButton.tonal(
                                  onPressed: () => widget.cartState.add(
                                    sku: item.id,
                                    title: item.name,
                                    priceCents: item.priceCents,
                                  ),
                                  child: Text(inCart ? 'Add More' : 'Add'),
                                ),
                              ),
                            );
                          },
                        );
                      },
                    ),
        );
      },
    );
  }
}
