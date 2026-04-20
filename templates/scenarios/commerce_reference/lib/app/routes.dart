import 'package:flutter/material.dart';

import '../features/auth/presentation/pages/auth_page.dart';
import '../features/cart/presentation/pages/cart_page.dart';
import '../features/catalog/presentation/pages/catalog_page.dart';
import '../features/profile/presentation/pages/profile_page.dart';

class AppRoutes {
  static const auth = '/auth';
  static const catalog = '/catalog';
  static const cart = '/cart';
  static const profile = '/profile';

  static const initialRoute = auth;
  static const appTitle = '{{ProjectName}} Commerce Reference';

  static final Map<String, WidgetBuilder> routes = {
    auth: (context) => const AuthPage(),
    catalog: (context) => const CatalogPage(),
    cart: (context) => const CartPage(),
    profile: (context) => const ProfilePage(),
  };
}
