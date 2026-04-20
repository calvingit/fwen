import '../entities/catalog_item.dart';

class GetCatalogItemsUseCase {
  const GetCatalogItemsUseCase();

  Future<List<CatalogItem>> call() async {
    return const [
      CatalogItem(
        id: '{{project_name}}-catalog-item-1',
        name: 'Starter Product',
        priceCents: 1999,
      ),
      CatalogItem(
        id: '{{project_name}}-catalog-item-2',
        name: 'Pro Product',
        priceCents: 4999,
      ),
    ];
  }
}
