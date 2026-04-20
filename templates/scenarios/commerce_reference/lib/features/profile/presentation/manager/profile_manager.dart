import 'package:flutter/foundation.dart';

import '../../domain/entities/profile_summary.dart';
import '../../domain/usecases/get_profile_summary_usecase.dart';

class ProfileManager extends ChangeNotifier {
  ProfileManager({GetProfileSummaryUseCase? getProfileSummary})
    : _getProfileSummary =
          getProfileSummary ?? const GetProfileSummaryUseCase();

  final GetProfileSummaryUseCase _getProfileSummary;

  ProfileSummary? summary;

  Future<void> load() async {
    summary = await _getProfileSummary();
    notifyListeners();
  }
}
