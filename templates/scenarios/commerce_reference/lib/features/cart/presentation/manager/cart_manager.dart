import 'package:flutter/foundation.dart';

import '../../domain/entities/cart_item.dart';
import '../../domain/usecases/get_cart_items_usecase.dart';

class CartManager extends ChangeNotifier {
  CartManager({GetCartItemsUseCase? getCartItems})
    : _getCartItems = getCartItems ?? const GetCartItemsUseCase();

  final GetCartItemsUseCase _getCartItems;

  List<CartItem> items = const [];

  int get totalItems => items.fold(0, (sum, item) => sum + item.quantity);

  Future<void> load() async {
    items = await _getCartItems();
    notifyListeners();
  }
}
