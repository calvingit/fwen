import 'package:flutter/material.dart';

import '../manager/cart_manager.dart';

class CartPage extends StatefulWidget {
  const CartPage({super.key});

  static const routeName = '/cart';

  @override
  State<CartPage> createState() => _CartPageState();
}

class _CartPageState extends State<CartPage> {
  late final CartManager _manager;

  @override
  void initState() {
    super.initState();
    _manager = CartManager();
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
          appBar: AppBar(title: const Text('Cart')),
          body: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Padding(
                padding: const EdgeInsets.all(16),
                child: Text('Items in cart: ${_manager.totalItems}'),
              ),
              Expanded(
                child: ListView.builder(
                  itemCount: _manager.items.length,
                  itemBuilder: (context, index) {
                    final item = _manager.items[index];

                    return ListTile(
                      title: Text(item.title),
                      subtitle: Text('Qty ${item.quantity}'),
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
