import '../entities/profile_summary.dart';

class GetProfileSummaryUseCase {
  const GetProfileSummaryUseCase();

  Future<ProfileSummary> call() async {
    return const ProfileSummary(
      name: 'Sample Member',
      email: 'member@{{project_name}}.app',
      memberSince: '2024-01',
    );
  }
}
