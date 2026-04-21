import 'package:flutter/foundation.dart';

import '../../data/repositories/in_memory_catalog_repository.dart';
import '../../domain/entities/catalog_item.dart';
import '../../domain/usecases/get_catalog_items_usecase.dart';

class CatalogManager extends ChangeNotifier {
  CatalogManager({GetCatalogItemsUseCase? getCatalogItems})
      : _getCatalogItems =
            getCatalogItems ?? GetCatalogItemsUseCase(InMemoryCatalogRepository());

  final GetCatalogItemsUseCase _getCatalogItems;

  List<CatalogItem> items = const [];
  bool isLoading = false;
  String? error;

  Future<void> load() async {
    isLoading = true;
    error = null;
    notifyListeners();
    try {
      items = await _getCatalogItems();
    } catch (e) {
      error = e.toString();
    }
    isLoading = false;
    notifyListeners();
  }
}
