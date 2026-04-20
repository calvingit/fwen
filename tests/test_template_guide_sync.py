"""Tests for template guide synchronization script."""

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SYNC_SCRIPT = REPO_ROOT / "scripts" / "sync_template_guide.py"


class TestTemplateGuideSync(unittest.TestCase):
    """Verify template guide stays aligned with template registry."""

    def test_template_guide_is_in_sync(self):
        """The sync script check mode should pass for committed docs."""
        result = subprocess.run(
            [sys.executable, str(SYNC_SCRIPT), "--check"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
