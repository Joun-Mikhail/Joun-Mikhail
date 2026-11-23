"""Design tokens shared by every generated SVG, so light and dark stay in sync."""

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "panel": "#161b22",
        "panel2": "#1c2330",
        "border": "#30363d",
        "grid": "#21262d",
        "text": "#e6edf3",
        "muted": "#8b949e",
        "accent": "#00d4ff",
        "accent2": "#8b5cf6",
        "ok": "#3fb950",
        "warn": "#d29922",
        "crit": "#f85149",
        "glow": "0.22",
    },
    "light": {
        "bg": "#ffffff",
        "panel": "#f6f8fa",
        "panel2": "#eef2f6",
        "border": "#d0d7de",
        "grid": "#e6eaef",
        "text": "#1f2328",
        "muted": "#59636e",
        "accent": "#0886a8",
        "accent2": "#6d28d9",
        "ok": "#1a7f37",
        "warn": "#9a6700",
        "crit": "#cf222e",
        "glow": "0.10",
    },
}

LANGUAGE_COLORS = {
    "Python": "#3572A5",
    "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a",
    "HTML": "#e34c26",
    "CSS": "#663399",
    "Shell": "#89e051",
    "Dockerfile": "#384d54",
    "Ruby": "#701516",
    "Mako": "#7e858d",
}
