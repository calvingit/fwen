import 'package:flutter/material.dart';

import '../features/cart/domain/cart_state.dart';
import '../features/cart/presentation/pages/cart_page.dart';
import '../features/catalog/presentation/pages/catalog_page.dart';
import '../features/profile/presentation/pages/profile_page.dart';

class ShellPage extends StatefulWidget {
  const ShellPage({super.key});

  static const routeName = '/shell';

  @override
  State<ShellPage> createState() => _ShellPageState();
}

class _ShellPageState extends State<ShellPage> {
  int _currentIndex = 0;
  final _cartState = CartState();

  @override
  void dispose() {
    _cartState.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final pages = [
      CatalogPage(cartState: _cartState),
      CartPage(cartState: _cartState),
      const ProfilePage(),
    ];

    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: pages,
      ),
      bottomNavigationBar: AnimatedBuilder(
        animation: _cartState,
        builder: (context, _) {
          return NavigationBar(
            selectedIndex: _currentIndex,
            onDestinationSelected: (index) => setState(() => _currentIndex = index),
            destinations: [
              const NavigationDestination(
                icon: Icon(Icons.storefront_outlined),
                selectedIcon: Icon(Icons.storefront),
                label: 'Catalog',
              ),
              NavigationDestination(
                icon: Badge(
                  isLabelVisible: _cartState.totalCount > 0,
                  label: Text('${_cartState.totalCount}'),
                  child: const Icon(Icons.shopping_cart_outlined),
                ),
                selectedIcon: Badge(
                  isLabelVisible: _cartState.totalCount > 0,
                  label: Text('${_cartState.totalCount}'),
                  child: const Icon(Icons.shopping_cart),
                ),
                label: 'Cart',
              ),
              const NavigationDestination(
                icon: Icon(Icons.person_outline),
                selectedIcon: Icon(Icons.person),
                label: 'Profile',
              ),
            ],
          );
        },
      ),
    );
  }
}
