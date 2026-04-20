class ServerException implements Exception {
  ServerException([this.message = 'Server Exception']);

  final String message;
}

class CacheException implements Exception {
  CacheException([this.message = 'Cache Exception']);

  final String message;
}
