import 'package:dio/dio.dart';

import '../utils/logger.dart';

class ApiClient {
  ApiClient({required String baseUrl})
    : _dio = Dio(
        BaseOptions(
          baseUrl: baseUrl,
          connectTimeout: const Duration(seconds: 5),
          receiveTimeout: const Duration(seconds: 3),
        ),
      ) {
    _dio.interceptors.add(
      LogInterceptor(
        requestBody: true,
        responseBody: true,
        logPrint: (obj) => appLogger.d(obj),
      ),
    );
  }

  final Dio _dio;

  Future<Response<dynamic>> get(
    String path, {
    Map<String, dynamic>? queryParameters,
  }) async {
    final response = await _dio.get<dynamic>(
      path,
      queryParameters: queryParameters,
    );
    return response;
  }

  Future<Response<dynamic>> post(
    String path, {
    dynamic data,
  }) async {
    final response = await _dio.post<dynamic>(path, data: data);
    return response;
  }
}
