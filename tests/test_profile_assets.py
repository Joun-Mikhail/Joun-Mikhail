import sys
import tempfile
import unittest
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import render_static  # noqa: E402
import render_status  # noqa: E402
from theme import THEMES  # noqa: E402

NOW = datetime(2026, 11, 23, 12, 0, tzinfo=timezone.utc)

API = {
    "/repos/me/api": {"description": "Serverless <API> & more", "language": "Python",
                      "pushed_at": "2026-11-21T12:00:00Z", "default_branch": "main"},
    "/repos/me/api/languages": {"Python": 9000, "Shell": 1000},
    "/repos/me/api/actions/workflows/ci.yml/runs?branch=main&per_page=1":
        {"workflow_runs": [{"status": "completed", "conclusion": "success"}]},
    "/repos/me/web": {"description": None, "language": "TypeScript",
                      "pushed_at": "2026-11-23T09:00:00Z", "default_branch": "trunk"},
    "/repos/me/web/languages": {"TypeScript": 10000},
    "/repos/me/web/actions/workflows/ci.yml/runs?branch=trunk&per_page=1":
        {"workflow_runs": [{"status": "completed", "conclusion": "failure"}]},
}


def fake_fetch(path):
    if path not in API:
        raise urllib.error.HTTPError(path, 404, "Not Found", None, None)
    return API[path]


class StatusBoardTest(unittest.TestCase):
    def test_collect_maps_ci_and_tolerates_missing_repos(self):
        rows = render_status.collect("me", [("api", "ci.yml"), ("web", "ci.yml"), ("gone", None)], fake_fetch)
        self.assertEqual([r["ci"] for r in rows], ["passing", "failing", None])
        self.assertEqual([r["ok"] for r in rows], [True, True, False])

    def test_missing_workflow_keeps_repo_data(self):
        rows = render_status.collect("me", [("api", "missing.yml")], fake_fetch)
        self.assertTrue(rows[0]["ok"])
        self.assertIsNone(rows[0]["ci"])

    def test_ci_state(self):
        self.assertIsNone(render_status.ci_state(None))
        self.assertEqual(render_status.ci_state({"status": "in_progress"}), "running")
        self.assertEqual(render_status.ci_state({"status": "completed", "conclusion": "cancelled"}), "failing")

    def test_relative_time(self):
        self.assertEqual(render_status.relative_time("2026-11-21T12:00:00Z", NOW), "2d ago")
        self.assertEqual(render_status.relative_time("2026-11-23T11:59:30Z", NOW), "just now")
        self.assertEqual(render_status.relative_time(None, NOW), "—")

    def test_language_share_sums_to_one(self):
        rows = [{"languages": {"Python": 3, "Go": 1}}, {"languages": {"Python": 1}}]
        shares = dict(render_status.language_share(rows))
        self.assertAlmostEqual(shares["Python"], 0.8)
        self.assertAlmostEqual(sum(shares.values()), 1.0)

    def test_render_is_valid_escaped_svg_in_both_themes(self):
        rows = render_status.collect("me", [("api", "ci.yml"), ("web", "ci.yml"), ("gone", None)], fake_fetch)
        for tokens in THEMES.values():
            svg = render_status.render(rows, NOW, tokens)
            ET.fromstring(svg)
            self.assertIn("Serverless &lt;API&gt; &amp; more", svg)
            self.assertIn("1 pipeline failing", svg)

    def test_main_fails_when_nothing_fetched(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(render_status.main(Path(tmp), fetch=fake_fetch), 1)


class StaticAssetsTest(unittest.TestCase):
    def test_committed_assets_match_generator(self):
        with tempfile.TemporaryDirectory() as tmp:
            render_static.main(Path(tmp))
            for generated in Path(tmp).glob("*.svg"):
                ET.parse(generated)
                committed = ROOT / "assets" / generated.name
                self.assertTrue(committed.exists(), f"{committed.name} missing; run scripts/render_static.py")
                self.assertEqual(committed.read_text(), generated.read_text(),
                                 f"{committed.name} is stale; run scripts/render_static.py")


if __name__ == "__main__":
    unittest.main()
