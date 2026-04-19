#!/usr/bin/env python3
"""
Test runner for Flutter Clean CLI tests.
"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import test modules
from tests.test_actions import TestPostCreationActions
from tests.test_cli import TestCli
from tests.test_config import TestConfig
from tests.test_feature_script import TestFeatureScript
from tests.test_generator import TestGenerateProject, TestProjectGenerator
from tests.test_main import TestMainEntrypoint, TestMainHelpers
from tests.test_prompts import TestPrompts
from tests.test_repository_assets import TestRepositoryAssets
from tests.test_utils import (
    TestCopyDirectory,
    TestCopyFileWithSubstitution,
    TestGetFlutterExecutable,
    TestPrintTree,
    TestValidateOutputDirectory,
)


def run_tests(verbosity=2):
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestCli))
    suite.addTests(loader.loadTestsFromTestCase(TestPostCreationActions))
    suite.addTests(loader.loadTestsFromTestCase(TestMainHelpers))
    suite.addTests(loader.loadTestsFromTestCase(TestMainEntrypoint))
    suite.addTests(loader.loadTestsFromTestCase(TestPrompts))
    suite.addTests(loader.loadTestsFromTestCase(TestGetFlutterExecutable))
    suite.addTests(loader.loadTestsFromTestCase(TestCopyFileWithSubstitution))
    suite.addTests(loader.loadTestsFromTestCase(TestCopyDirectory))
    suite.addTests(loader.loadTestsFromTestCase(TestValidateOutputDirectory))
    suite.addTests(loader.loadTestsFromTestCase(TestPrintTree))
    suite.addTests(loader.loadTestsFromTestCase(TestProjectGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestGenerateProject))
    suite.addTests(loader.loadTestsFromTestCase(TestFeatureScript))
    suite.addTests(loader.loadTestsFromTestCase(TestRepositoryAssets))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    return result


def main():
    """Main entry point."""
    print("=" * 70)
    print("Flutter Clean CLI - Test Suite")
    print("=" * 70)
    print()

    result = run_tests()

    print()
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 70)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
