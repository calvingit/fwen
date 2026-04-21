import 'package:flutter/material.dart';

import '../../domain/cart_state.dart';

class CartPage extends StatelessWidget {
  const CartPage({super.key, required this.cartState});

  final CartState cartState;

  static const routeName = '/cart';

  String _formatPrice(int cents) => '\$${(cents / 100).toStringAsFixed(2)}';

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: cartState,
      builder: (context, _) {
        final items = cartState.items;

        return Scaffold(
          appBar: AppBar(
            title: const Text('Cart'),
            actions: [
              if (items.isNotEmpty)
                IconButton(
                  icon: const Icon(Icons.delete_sweep_outlined),
                  tooltip: 'Clear cart',
                  onPressed: cartState.clear,
                ),
            ],
          ),
          body: items.isEmpty
              ? const Center(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.shopping_cart_outlined,
                          size: 64, color: Colors.grey),
                      SizedBox(height: 16),
                      Text('Your cart is empty',
                          style: TextStyle(color: Colors.grey)),
                    ],
                  ),
                )
              : Column(
                  children: [
                    Expanded(
                      child: ListView.builder(
                        itemCount: items.length,
                        itemBuilder: (context, index) {
                          final item = items[index];
                          return ListTile(
                            title: Text(item.title),
                            subtitle: Text(
                                '${_formatPrice(item.priceCents)} × ${item.quantity}'),
                            trailing: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Text(
                                  _formatPrice(item.totalCents),
                                  style: Theme.of(context).textTheme.titleMedium,
                                ),
                                const SizedBox(width: 4),
                                IconButton(
                                  icon: const Icon(Icons.remove_circle_outline),
                                  onPressed: () => cartState.remove(item.sku),
                                ),
                              ],
                            ),
                          );
                        },
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        border: Border(
                            top: BorderSide(
                                color: Theme.of(context).dividerColor)),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('Total',
                              style: TextStyle(
                                  fontWeight: FontWeight.bold, fontSize: 16)),
                          Text(
                            _formatPrice(cartState.totalCents),
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                        ],
                      ),
                    ),
                    SafeArea(
                      child: Padding(
                        padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
                        child: SizedBox(
                          width: double.infinity,
                          child: FilledButton(
                            onPressed: () {
                              cartState.clear();
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                    content: Text('Order placed — thank you!')),
                              );
                            },
                            child: const Text('Place Order'),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
        );
      },
    );
  }
}
