import '../entities/cart_item.dart';

class GetCartItemsUseCase {
  const GetCartItemsUseCase();

  Future<List<CartItem>> call() async {
    return const [
      CartItem(
        sku: '{{project_name}}-catalog-item-1',
        title: 'Starter Product',
        quantity: 1,
        priceCents: 1999,
      ),
    ];
  }
}
