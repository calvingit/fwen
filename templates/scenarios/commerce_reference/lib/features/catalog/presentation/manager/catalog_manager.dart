import 'package:flutter/foundation.dart';

import '../../domain/entities/catalog_item.dart';
import '../../domain/usecases/get_catalog_items_usecase.dart';

class CatalogManager extends ChangeNotifier {
  CatalogManager({GetCatalogItemsUseCase? getCatalogItems})
    : _getCatalogItems = getCatalogItems ?? const GetCatalogItemsUseCase();

  final GetCatalogItemsUseCase _getCatalogItems;

  List<CatalogItem> items = const [];

  Future<void> load() async {
    items = await _getCatalogItems();
    notifyListeners();
  }
}
