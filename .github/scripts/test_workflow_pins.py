"""Regression pins for the analyzer publishing workflow and the frozen page.

Standard library only. Run from the repo root:

    python3 -m unittest discover -s .github/scripts -p "test_*.py" -v
"""

import hashlib
import pathlib
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
WORKFLOW = REPO / ".github/workflows/update-bigfix-relevance-analyzer-playground.yaml"
FROZEN_PAGE = REPO / "files/bigfix-relevance-analyzer-playground.html"
# The single-file playground as of v1.38.1. It is frozen: the site no longer
# updates it, and it will become a redirect in a later, separate change.
FROZEN_PAGE_SHA256 = "d52bfc94fe44611d26ca3ba6f2b89acb2f7ce41496c0d79fd5e1457218b466b4"


class FrozenPageTest(unittest.TestCase):
    def test_frozen_page_is_unchanged(self):
        digest = hashlib.sha256(FROZEN_PAGE.read_bytes()).hexdigest()
        self.assertEqual(digest, FROZEN_PAGE_SHA256)


class WorkflowTriggersTest(unittest.TestCase):
    """The analyzer repo's release dispatches this workflow by file name."""

    def setUp(self):
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def test_file_name(self):
        self.assertTrue(WORKFLOW.is_file())

    def test_weekly_schedule(self):
        self.assertIn("schedule:", self.text)
        self.assertIn('- cron: "17 5 * * 0"', self.text)

    def test_dispatch_with_optional_version(self):
        self.assertIn("workflow_dispatch:", self.text)
        self.assertIn("version:", self.text)
        self.assertIn("required: false", self.text)

    def test_pull_request_dry_run_never_pushes(self):
        self.assertIn("pull_request:", self.text)
        # The push is guarded by an explicit pull_request check.
        self.assertIn('"$GITHUB_EVENT_NAME" = "pull_request"', self.text)
        push_at = self.text.index("git push")
        guard_at = self.text.rindex('"$GITHUB_EVENT_NAME" = "pull_request"', 0, push_at)
        self.assertLess(guard_at, push_at)

    def test_resolves_release_from_analyzer_repo(self):
        self.assertIn("--repo jgstew/bigfix-relevance-analyzer", self.text)
        self.assertIn("SHA256SUMS.txt", self.text)


if __name__ == "__main__":
    unittest.main()
