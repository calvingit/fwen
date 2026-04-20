class CartItem {
  const CartItem({
    required this.sku,
    required this.title,
    required this.quantity,
  });

  final String sku;
  final String title;
  final int quantity;
}
