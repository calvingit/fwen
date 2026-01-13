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
from tests.test_config import TestConfig
from tests.test_utils import (
    TestCopyDirectory,
    TestCopyFileWithSubstitution,
    TestGetFlutterExecutable,
    TestPrintTree,
    TestValidateOutputDirectory,
)
from tests.test_generator import TestGenerateProject, TestProjectGenerator


def run_tests(verbosity=2):
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestGetFlutterExecutable))
    suite.addTests(loader.loadTestsFromTestCase(TestCopyFileWithSubstitution))
    suite.addTests(loader.loadTestsFromTestCase(TestCopyDirectory))
    suite.addTests(loader.loadTestsFromTestCase(TestValidateOutputDirectory))
    suite.addTests(loader.loadTestsFromTestCase(TestPrintTree))
    suite.addTests(loader.loadTestsFromTestCase(TestProjectGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestGenerateProject))

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
