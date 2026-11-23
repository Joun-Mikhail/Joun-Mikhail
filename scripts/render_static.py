"""Render the hand-designed profile SVGs (hero, metrics, footer) in light and dark variants.

Usage: python scripts/render_static.py [out_dir]   (default: assets/)
"""

import math
import random
import sys
from pathlib import Path
from string import Template

sys.path.insert(0, str(Path(__file__).resolve().parent))
from theme import MONO, SANS, THEMES  # noqa: E402

REDUCED_MOTION = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def text_width(text: str, size: float, mono: bool = False) -> float:
    return len(text) * size * (0.61 if mono else 0.52)


def chip(x: float, y: float, label: str, t: dict) -> tuple[str, float]:
    w = text_width(label, 13) + 30
    svg = (
        f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="{t["panel2"]}" stroke="{t["border"]}"/>'
        f'<text x="{x + 15:.0f}" y="{y + 20}" class="sans" font-size="13" fill="{t["text"]}">{label}</text>'
    )
    return svg, w


def sparkline(width: int, height: int, seed: int = 7) -> str:
    """A seamless (periodic) latency trace, drawn twice so it can scroll forever."""
    rng = random.Random(seed)
    step = 12
    n = width // step
    ys = []
    for i in range(n + 1):
        base = 0.62 + 0.10 * math.sin(i / n * math.tau * 2)
        ys.append(base + rng.uniform(-0.08, 0.08))
    spike = int(n * 0.68)
    ys[spike - 1] = 0.30
    ys[spike] = 0.08
    ys[spike + 1] = 0.36
    ys[-1] = ys[0]
    points = []
    for copy in range(2):
        for i, y in enumerate(ys):
            if copy and i == 0:
                continue
            points.append(f"{copy * width + i * step:.0f},{y * height:.1f}")
    return "M" + " L".join(points)


HERO = Template("""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="420" viewBox="0 0 1200 420" role="img" aria-labelledby="title desc">
<title id="title">Joun Mikhail — Cloud Support &amp; IT Support Engineer</title>
<desc id="desc">Animated banner: an AWS serverless topology with requests flowing from client through API Gateway and Lambda to DynamoDB, and an alarm path through CloudWatch to SNS.</desc>
<defs>
  <linearGradient id="name" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="$text"/><stop offset="0.55" stop-color="$accent"/><stop offset="1" stop-color="$accent2"/>
  </linearGradient>
  <radialGradient id="glowA" cx="0.18" cy="0.12" r="0.55">
    <stop offset="0" stop-color="$accent" stop-opacity="$glow"/><stop offset="1" stop-color="$accent" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowB" cx="0.86" cy="0.95" r="0.5">
    <stop offset="0" stop-color="$accent2" stop-opacity="$glow"/><stop offset="1" stop-color="$accent2" stop-opacity="0"/>
  </radialGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1.5" cy="1.5" r="1.1" fill="$grid"/>
  </pattern>
  <linearGradient id="area" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="$accent" stop-opacity="0.28"/><stop offset="1" stop-color="$accent" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="card"><rect x="1" y="1" width="1198" height="418" rx="18"/></clipPath>
  <clipPath id="spark"><rect x="724" y="292" width="412" height="64"/></clipPath>
  <path id="req" d="M780,116 L1080,116 L1080,210"/>
  <path id="alarm" d="M1080,116 C1040,168 930,158 930,210 L780,210"/>
</defs>
<style>
  .sans { font-family: $sans; }
  .mono { font-family: $mono; }
  .up { animation: up .9s cubic-bezier(.2,.7,.2,1) both; }
  .d1 { animation-delay: .08s } .d2 { animation-delay: .18s } .d3 { animation-delay: .28s } .d4 { animation-delay: .38s } .d5 { animation-delay: .5s }
  @keyframes up { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
  .pulse { transform-box: fill-box; transform-origin: center; animation: pulse 2s ease-out infinite; }
  @keyframes pulse { 0% { transform: scale(1); opacity: .9 } 100% { transform: scale(3.2); opacity: 0 } }
  .flow { stroke-dasharray: 4 7; animation: flow 1.2s linear infinite; }
  @keyframes flow { to { stroke-dashoffset: -22; } }
  .scroll { animation: scroll 9s linear infinite; }
  @keyframes scroll { to { transform: translateX(-412px); } }
  .sns { animation: flash 6s linear infinite; }
  @keyframes flash { 0%,49% { stroke: $border } 52%,64% { stroke: $crit } 70%,100% { stroke: $border } }
  .ping { animation: ping 6s linear infinite; }
  @keyframes ping { 0%,49% { opacity: 0 } 52%,64% { opacity: 1 } 70%,100% { opacity: 0 } }
  $reduced
</style>

<g clip-path="url(#card)">
  <rect width="1200" height="420" fill="$bg"/>
  <rect width="1200" height="420" fill="url(#dots)"/>
  <rect width="1200" height="420" fill="url(#glowA)"/>
  <rect width="1200" height="420" fill="url(#glowB)"/>
</g>
<rect x="1" y="1" width="1198" height="418" rx="18" fill="none" stroke="$border"/>

<!-- left: identity -->
<g class="up">
  <rect x="56" y="44" width="330" height="30" rx="15" fill="$panel2" stroke="$border"/>
  <circle cx="76" cy="59" r="4.5" fill="$ok" class="pulse"/>
  <circle cx="76" cy="59" r="4.5" fill="$ok"/>
  <text x="92" y="64" class="mono" font-size="12" letter-spacing="1.4" fill="$text">AVAILABLE · OPEN TO EU RELOCATION</text>
</g>
<text x="54" y="152" class="sans up d1" font-size="64" font-weight="800" letter-spacing="-1.5" fill="url(#name)">Joun Mikhail</text>
<text x="56" y="198" class="sans up d2" font-size="25" font-weight="600" fill="$text">Cloud Support Engineer  ·  IT Support Engineer</text>
<text x="56" y="236" class="mono up d3" font-size="15" fill="$accent">AWS serverless  /  monitoring &amp; incident response  /  automation</text>
<g class="up d4">$chips</g>
<text x="56" y="372" class="mono up d5" font-size="14" fill="$muted">&gt; "If it breaks at 3am, I want to know before the users do."</text>

<!-- right: live topology -->
<g class="up d2">
  <rect x="700" y="40" width="460" height="340" rx="14" fill="$panel" stroke="$border"/>
  <circle cx="722" cy="62" r="4" fill="$crit" opacity=".8"/><circle cx="736" cy="62" r="4" fill="$warn" opacity=".8"/><circle cx="750" cy="62" r="4" fill="$ok" opacity=".8"/>
  <text x="768" y="66" class="mono" font-size="11" fill="$muted">serverless-api · request path</text>
  <text x="1140" y="66" text-anchor="end" class="mono" font-size="11" fill="$muted">eu-central-1</text>
  <line x1="700" y1="78" x2="1160" y2="78" stroke="$border"/>

  <g fill="none" stroke="$muted" stroke-width="1.6" stroke-opacity=".7">
    <path class="flow" d="M836,116 L874,116"/>
    <path class="flow" d="M986,116 L1024,116"/>
    <path class="flow" d="M1080,136 L1080,190"/>
    <path class="flow" d="M1040,136 C1040,168 930,158 930,190"/>
    <path class="flow" d="M874,210 L836,210"/>
  </g>

  <g fill="$accent">
    <circle r="4.5"><animateMotion dur="3.2s" repeatCount="indefinite" begin="0s"><mpath href="#req" xlink:href="#req"/></animateMotion></circle>
    <circle r="4.5"><animateMotion dur="3.2s" repeatCount="indefinite" begin="1.07s"><mpath href="#req" xlink:href="#req"/></animateMotion></circle>
    <circle r="4.5"><animateMotion dur="3.2s" repeatCount="indefinite" begin="2.13s"><mpath href="#req" xlink:href="#req"/></animateMotion></circle>
  </g>
  <circle r="5" fill="$crit"><animateMotion dur="6s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.5;1" calcMode="linear"><mpath href="#alarm" xlink:href="#alarm"/></animateMotion></circle>

  $nodes
  <rect x="724" y="190" width="112" height="40" rx="9" fill="none" stroke-width="1.6" class="sns"/>
  <text x="780" y="248" text-anchor="middle" class="mono ping" font-size="10.5" fill="$crit">ALARM → on-call</text>

  <line x1="720" y1="266" x2="1140" y2="266" stroke="$border"/>
  <text x="724" y="286" class="mono" font-size="11" fill="$muted">p95 latency</text>
  <text x="1136" y="286" text-anchor="end" class="mono" font-size="11" fill="$warn">- - SLO</text>
  <line x1="724" y1="312" x2="1136" y2="312" stroke="$warn" stroke-dasharray="3 5" stroke-opacity=".7"/>
  <g clip-path="url(#spark)">
    <g class="scroll">
      <g transform="translate(724,292)">
        <path d="$spark L824,64 L0,64 Z" fill="url(#area)"/>
        <path d="$spark" fill="none" stroke="$accent" stroke-width="1.8" stroke-linejoin="round"/>
      </g>
    </g>
  </g>
</g>
</svg>
""")

NODES = [
    ("Client", 724, 96, "muted"),
    ("API Gateway", 874, 96, "accent2"),
    ("Lambda", 1024, 96, "warn"),
    ("SNS alert", 724, 190, "crit"),
    ("CloudWatch", 874, 190, "accent2"),
    ("DynamoDB", 1024, 190, "accent"),
]


def render_hero(t: dict) -> str:
    chips, x = [], 56.0
    for label in ("Brno, Czech Republic", "English · Arabic", "AWS · Python · Docker · Linux"):
        svg, w = chip(x, 276, label, t)
        chips.append(svg)
        x += w + 10
    nodes = []
    for label, nx, ny, color in NODES:
        nodes.append(
            f'<rect x="{nx}" y="{ny}" width="112" height="40" rx="9" fill="{t["panel2"]}" stroke="{t["border"]}"/>'
            f'<rect x="{nx + 12}" y="{ny + 16}" width="8" height="8" rx="2" fill="{t[color]}"/>'
            f'<text x="{nx + 28}" y="{ny + 25}" class="sans" font-size="13" font-weight="600" fill="{t["text"]}">{label}</text>'
        )
    return HERO.substitute(
        t, sans=SANS, mono=MONO, reduced=REDUCED_MOTION, chips="".join(chips), nodes="\n  ".join(nodes),
        spark=sparkline(412, 64),
    )


METRICS = [
    ("400+", "automated tests", "across 4 projects"),
    ("97%", "test coverage", "CareerFlow backend"),
    ("8", "CI/CD workflows", "test · deploy · smoke · keep-warm"),
    ("0", "long-lived AWS keys", "deploys use GitHub OIDC"),
]


def render_metrics(t: dict) -> str:
    tiles = []
    w, gap = 286, 18
    for i, (value, label, sub) in enumerate(METRICS):
        x = 1 + i * (w + gap)
        delay = f"{0.1 * i:.1f}s"
        tiles.append(f"""
  <g class="up" style="animation-delay:{delay}">
    <rect x="{x}" y="1" width="{w}" height="134" rx="14" fill="{t["panel"]}" stroke="{t["border"]}"/>
    <rect x="{x + 22}" y="1" width="56" height="3" rx="1.5" fill="url(#bar)" class="grow" style="animation-delay:{delay}"/>
    <text x="{x + 22}" y="64" class="sans" font-size="42" font-weight="800" letter-spacing="-1" fill="url(#num)">{value}</text>
    <text x="{x + 22}" y="94" class="sans" font-size="16" font-weight="600" fill="{t["text"]}">{label}</text>
    <text x="{x + 22}" y="117" class="mono" font-size="12" fill="{t["muted"]}">{sub}</text>
  </g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="136" viewBox="0 0 1200 136" role="img" aria-labelledby="title">
<title id="title">At a glance: 400+ automated tests across 4 projects; 97% backend test coverage on CareerFlow; 8 CI/CD workflows; 0 long-lived AWS keys, deploys use GitHub OIDC.</title>
<defs>
  <linearGradient id="num" x1="0" x2="1"><stop offset="0" stop-color="{t["accent"]}"/><stop offset="1" stop-color="{t["accent2"]}"/></linearGradient>
  <linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{t["accent"]}"/><stop offset="1" stop-color="{t["accent2"]}"/></linearGradient>
</defs>
<style>
  .sans {{ font-family: {SANS}; }} .mono {{ font-family: {MONO}; }}
  .up {{ animation: up .8s cubic-bezier(.2,.7,.2,1) both; }}
  @keyframes up {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
  .grow {{ transform-box: fill-box; transform-origin: left; animation: grow 1.2s cubic-bezier(.2,.7,.2,1) both; }}
  @keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
  {REDUCED_MOTION}
</style>{"".join(tiles)}
</svg>
"""


def heartbeat_path(width: int, mid: float) -> str:
    beat = [(0, 0), (14, 0), (20, -6), (26, 0), (32, 0), (37, 8), (43, -34), (49, 18), (55, 0), (66, 0), (74, -9), (84, 0)]
    pts, x = [], 0
    period = 150
    while x < width:
        for dx, dy in beat:
            if x + dx <= width:
                pts.append(f"{x + dx},{mid + dy}")
        x += period
        pts.append(f"{min(x, width)},{mid}")
    return "M" + " L".join(pts)


def render_footer(t: dict) -> str:
    path = heartbeat_path(1200, 108)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="140" viewBox="0 0 1200 140" role="img" aria-labelledby="title">
<title id="title">Let's keep your systems running.</title>
<defs>
  <linearGradient id="fade" x1="0" x2="1">
    <stop offset="0" stop-color="{t["accent"]}" stop-opacity="0"/><stop offset=".2" stop-color="{t["accent"]}"/>
    <stop offset=".8" stop-color="{t["accent2"]}"/><stop offset="1" stop-color="{t["accent2"]}" stop-opacity="0"/>
  </linearGradient>
</defs>
<style>
  .sans {{ font-family: {SANS}; }} .mono {{ font-family: {MONO}; }}
  .trace {{ stroke-dasharray: 2600; stroke-dashoffset: 2600; animation: draw 5s linear infinite; }}
  @keyframes draw {{ 0% {{ stroke-dashoffset: 2600; }} 70%,100% {{ stroke-dashoffset: 0; }} }}
  {REDUCED_MOTION}
</style>
<text x="600" y="36" text-anchor="middle" class="sans" font-size="22" font-weight="700" fill="{t["text"]}">Let's keep your systems running.</text>
<text x="600" y="60" text-anchor="middle" class="mono" font-size="12" fill="{t["muted"]}">uptime is a feature · alerts before users notice · runbooks over heroics</text>
<path d="{path}" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>
<path d="{path}" fill="none" stroke="url(#fade)" stroke-width="2" stroke-linejoin="round" class="trace"/>
</svg>
"""


RENDERERS = {"hero": render_hero, "metrics": render_metrics, "footer": render_footer}


def main(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, render in RENDERERS.items():
        for mode, tokens in THEMES.items():
            (out_dir / f"{name}-{mode}.svg").write_text(render(tokens), encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "assets")
