class CartItem {
  const CartItem({
    required this.sku,
    required this.title,
    required this.quantity,
    required this.priceCents,
  });

  final String sku;
  final String title;
  final int quantity;
  final int priceCents;

  int get totalCents => priceCents * quantity;

  CartItem copyWith({int? quantity}) => CartItem(
        sku: sku,
        title: title,
        quantity: quantity ?? this.quantity,
        priceCents: priceCents,
      );
}
