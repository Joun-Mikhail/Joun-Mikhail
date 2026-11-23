"""Build a status-page style SVG for featured repositories from live GitHub API data.

Runs daily in GitHub Actions (see .github/workflows/status-board.yml). Standard library only.
Usage: GITHUB_TOKEN=... python scripts/render_status.py [out_dir]   (default: dist/)
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
from theme import LANGUAGE_COLORS, MONO, SANS, THEMES  # noqa: E402

OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER", "Joun-Mikhail")
FEATURED = [
    ("careerflow", "ci.yml"),
    ("device-registry-serverless-api", "ci.yml"),
    ("iot-monitoring-system", None),
    ("service-watchdog", None),
]

Fetch = Callable[[str], object]


def github_fetch(path: str) -> object:
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if token := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def ci_state(run: dict | None) -> str | None:
    if not run:
        return None
    if run.get("status") != "completed":
        return "running"
    return "passing" if run.get("conclusion") == "success" else "failing"


def collect(owner: str, featured: list, fetch: Fetch) -> list[dict]:
    rows = []
    for name, workflow in featured:
        row = {"name": name, "ok": False, "ci": None, "languages": {}}
        try:
            repo = fetch(f"/repos/{owner}/{name}")
            row.update(
                ok=True,
                description=repo.get("description") or "",
                language=repo.get("language"),
                pushed_at=repo.get("pushed_at"),
            )
            row["languages"] = fetch(f"/repos/{owner}/{name}/languages") or {}
            if workflow:
                branch = repo.get("default_branch", "main")
                runs = fetch(f"/repos/{owner}/{name}/actions/workflows/{workflow}/runs?branch={branch}&per_page=1")
                row["ci"] = ci_state((runs.get("workflow_runs") or [None])[0])
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as exc:
            print(f"warning: {name}: {exc}", file=sys.stderr)
        rows.append(row)
    return rows


def relative_time(iso: str | None, now: datetime) -> str:
    if not iso:
        return "—"
    then = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    secs = max(0, int((now - then).total_seconds()))
    for unit, size in (("y", 31_536_000), ("mo", 2_592_000), ("d", 86_400), ("h", 3_600), ("m", 60)):
        if secs >= size:
            return f"{secs // size}{unit} ago"
    return "just now"


def truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def language_share(rows: list[dict], top: int = 5) -> list[tuple[str, float]]:
    totals: dict[str, int] = {}
    for row in rows:
        for lang, size in row["languages"].items():
            totals[lang] = totals.get(lang, 0) + size
    grand = sum(totals.values())
    if not grand:
        return []
    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    shares = [(lang, size / grand) for lang, size in ranked[:top]]
    rest = 1 - sum(s for _, s in shares)
    if rest > 0.005:
        shares.append(("Other", rest))
    return shares


PILL = {"passing": "ok", "failing": "crit", "running": "warn"}
ROW_H = 58
TOP = 84


def render(rows: list[dict], now: datetime, t: dict) -> str:
    shares = language_share(rows)
    height = TOP + ROW_H * len(rows) + (96 if shares else 20)
    states = [r["ci"] for r in rows if r["ci"]]
    failing = sum(s == "failing" for s in states)
    summary, summary_color = (
        (f"{failing} pipeline{'s' * (failing > 1)} failing", t["crit"]) if failing
        else (f"all {len(states)} pipelines passing", t["ok"]) if states
        else ("no pipelines tracked", t["muted"])
    )
    out = [f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title">
<title id="title">Repository status board for {escape(OWNER)}, generated {now:%Y-%m-%d} UTC: {escape(summary)}.</title>
<style>
  .sans {{ font-family: {SANS}; }} .mono {{ font-family: {MONO}; }}
  .pulse {{ transform-box: fill-box; transform-origin: center; animation: pulse 2s ease-out infinite; }}
  @keyframes pulse {{ 0% {{ transform: scale(1); opacity: .9 }} 100% {{ transform: scale(3); opacity: 0 }} }}
  .row {{ animation: in .6s ease-out both; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateX(-8px); }} to {{ opacity: 1; transform: none; }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<rect x="1" y="1" width="1198" height="{height - 2}" rx="16" fill="{t["panel"]}" stroke="{t["border"]}"/>
<circle cx="32" cy="36" r="5" fill="{summary_color}" class="pulse"/><circle cx="32" cy="36" r="5" fill="{summary_color}"/>
<text x="48" y="42" class="sans" font-size="18" font-weight="700" fill="{t["text"]}">Repository status</text>
<text x="222" y="42" class="mono" font-size="12" fill="{t["muted"]}">auto-generated {now:%Y-%m-%d %H:%M} UTC by GitHub Actions</text>
<text x="1172" y="42" text-anchor="end" class="mono" font-size="12" font-weight="600" fill="{summary_color}">{escape(summary)}</text>
<line x1="1" y1="{TOP - 16}" x2="1199" y2="{TOP - 16}" stroke="{t["border"]}"/>"""]

    for i, row in enumerate(rows):
        y = TOP + i * ROW_H
        state = row["ci"]
        dot = t[PILL[state]] if state else (t["accent"] if row["ok"] else t["muted"])
        desc = row.get("description") or ("data unavailable" if not row["ok"] else "")
        out.append(f'<g class="row" style="animation-delay:{0.08 * i:.2f}s">')
        out.append(f'<circle cx="32" cy="{y + 20}" r="5" fill="{dot}"/>')
        out.append(f'<text x="48" y="{y + 25}" class="sans" font-size="15" font-weight="600" fill="{t["text"]}">{escape(row["name"])}</text>')
        out.append(f'<text x="48" y="{y + 44}" class="mono" font-size="12" fill="{t["muted"]}">{escape(truncate(desc, 92))}</text>')
        if lang := row.get("language"):
            out.append(f'<circle cx="842" cy="{y + 20}" r="5" fill="{LANGUAGE_COLORS.get(lang, t["muted"])}"/>')
            out.append(f'<text x="854" y="{y + 25}" class="sans" font-size="13" fill="{t["text"]}">{escape(lang)}</text>')
        if state:
            color = t[PILL[state]]
            out.append(f'<rect x="966" y="{y + 7}" width="86" height="24" rx="12" fill="{color}" fill-opacity=".14" stroke="{color}" stroke-opacity=".5"/>')
            out.append(f'<text x="1009" y="{y + 23}" text-anchor="middle" class="mono" font-size="11.5" font-weight="600" fill="{color}">{state}</text>')
        out.append(f'<text x="1172" y="{y + 25}" text-anchor="end" class="mono" font-size="12" fill="{t["muted"]}">{relative_time(row.get("pushed_at"), now)}</text>')
        out.append("</g>")
        if i < len(rows) - 1:
            out.append(f'<line x1="24" y1="{y + ROW_H - 4}" x2="1176" y2="{y + ROW_H - 4}" stroke="{t["grid"]}"/>')

    if shares:
        y = TOP + len(rows) * ROW_H + 8
        out.append(f'<text x="24" y="{y + 4}" class="mono" font-size="11" fill="{t["muted"]}">LANGUAGES ACROSS FEATURED REPOS</text>')
        out.append(f'<clipPath id="bar"><rect x="24" y="{y + 16}" width="1152" height="10" rx="5"/></clipPath><g clip-path="url(#bar)">')
        x = 24.0
        for lang, share in shares:
            w = 1152 * share
            out.append(f'<rect x="{x:.1f}" y="{y + 16}" width="{w + 0.5:.1f}" height="10" fill="{LANGUAGE_COLORS.get(lang, t["border"])}" stroke="{t["panel"]}" stroke-width="2"/>')
            x += w
        out.append("</g>")
        x = 24.0
        for lang, share in shares:
            label = f"{lang} {share * 100:.1f}%"
            out.append(f'<circle cx="{x + 5:.0f}" cy="{y + 47}" r="5" fill="{LANGUAGE_COLORS.get(lang, t["border"])}"/>')
            out.append(f'<text x="{x + 16:.0f}" y="{y + 51}" class="sans" font-size="12.5" fill="{t["text"]}">{escape(label)}</text>')
            x += 16 + len(label) * 7.2 + 22
    out.append("</svg>\n")
    return "\n".join(out)


def main(out_dir: Path, fetch: Fetch = github_fetch) -> int:
    rows = collect(OWNER, FEATURED, fetch)
    if not any(r["ok"] for r in rows):
        print("error: no repository data could be fetched", file=sys.stderr)
        return 1
    now = datetime.now(timezone.utc)
    out_dir.mkdir(parents=True, exist_ok=True)
    for mode, tokens in THEMES.items():
        (out_dir / f"status-{mode}.svg").write_text(render(rows, now, tokens), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist")))
