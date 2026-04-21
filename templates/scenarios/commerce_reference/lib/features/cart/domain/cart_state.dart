import 'package:flutter/foundation.dart';

import 'entities/cart_item.dart';

class CartState extends ChangeNotifier {
  final _items = <String, CartItem>{};

  List<CartItem> get items => _items.values.toList();

  int get totalCount => _items.values.fold(0, (sum, item) => sum + item.quantity);

  int get totalCents => _items.values.fold(0, (sum, item) => sum + item.totalCents);

  void add({required String sku, required String title, required int priceCents}) {
    final existing = _items[sku];
    _items[sku] = existing != null
        ? existing.copyWith(quantity: existing.quantity + 1)
        : CartItem(sku: sku, title: title, quantity: 1, priceCents: priceCents);
    notifyListeners();
  }

  void remove(String sku) {
    _items.remove(sku);
    notifyListeners();
  }

  void clear() {
    _items.clear();
    notifyListeners();
  }
}
