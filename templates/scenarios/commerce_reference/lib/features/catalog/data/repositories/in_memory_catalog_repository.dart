import '../../domain/entities/catalog_item.dart';
import '../../domain/repositories/catalog_repository.dart';

class InMemoryCatalogRepository implements CatalogRepository {
  @override
  Future<List<CatalogItem>> getItems() async {
    await Future.delayed(const Duration(milliseconds: 300));
    return const [
      CatalogItem(id: '{{project_name}}-item-1', name: 'Starter Product', priceCents: 1999),
      CatalogItem(id: '{{project_name}}-item-2', name: 'Pro Product', priceCents: 4999),
      CatalogItem(id: '{{project_name}}-item-3', name: 'Enterprise Package', priceCents: 9999),
      CatalogItem(id: '{{project_name}}-item-4', name: 'Team Plan', priceCents: 14999),
    ];
  }
}
