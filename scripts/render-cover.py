#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""Render images/cover.png from the theme JSON, so the cover always shows the shipped colors.

Needs Google Chrome (headless screenshot).
"""

import html
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WIDTH, HEIGHT = 1600, 1000

CODE = [
    [("comment", "// Resolve the palette for the active workspace.")],
    [("keyword", "import"), ("plain", " { "), ("variable", "createTheme"), ("plain", " } "), ("keyword", "from"), ("plain", " "), ("string", "'./theme'")],
    [],
    [("keyword", "export"), ("plain", " "), ("storage", "interface"), ("plain", " "), ("type", "Workspace"), ("plain", " {")],
    [("plain", "  "), ("variable", "name"), ("operator", ":"), ("plain", " "), ("type", "string")],
    [("plain", "  "), ("variable", "tabs"), ("operator", ":"), ("plain", " "), ("type", "number")],
    [("plain", "}")],
    [],
    [("keyword", "export"), ("plain", " "), ("storage", "function"), ("plain", " "), ("function", "openWorkspace"), ("plain", "("), ("variable", "ws"), ("operator", ":"), ("plain", " "), ("type", "Workspace"), ("plain", ") {")],
    [("plain", "  "), ("storage", "const"), ("plain", " "), ("variable", "theme"), ("plain", " "), ("operator", "="), ("plain", " "), ("function", "createTheme"), ("plain", "({ "), ("variable", "contrast"), ("operator", ":"), ("plain", " "), ("number", "0.92"), ("plain", " })")],
    [("plain", "  "), ("keyword", "if"), ("plain", " ("), ("variable", "ws"), ("plain", "."), ("variable", "tabs"), ("plain", " "), ("operator", ">"), ("plain", " "), ("number", "12"), ("plain", ") "), ("keyword", "return"), ("plain", " "), ("variable", "theme"), ("plain", "."), ("function", "compact"), ("plain", "()")],
    [("plain", "  "), ("keyword", "return"), ("plain", " { "), ("operator", "..."), ("variable", "theme"), ("plain", ", "), ("variable", "title"), ("operator", ":"), ("plain", " "), ("variable", "ws"), ("plain", "."), ("variable", "name"), ("plain", " "), ("operator", "+"), ("plain", " "), ("string", "' \u2014 Orca'"), ("plain", " }")],
    [("plain", "}")],
]
SCOPES = {
    "comment": "Comments",
    "keyword": "Keywords",
    "storage": "Storage modifiers",
    "operator": "Operators",
    "string": "Strings",
    "function": "Functions",
    "type": "Types",
    "number": "Numbers",
    "variable": "Variables",
}
TREE = [(0, "src", False), (1, "components", False), (2, "Sidebar.tsx", False), (2, "theme.ts", True), (1, "server", False), (2, "router.ts", False), (0, "package.json", False), (0, "README.md", False), (0, "tsconfig.json", False)]


def load(mode: str) -> tuple[dict, dict, dict]:
    theme = json.loads((ROOT / f"themes/gruvbox-material-mix-{mode}.json").read_text())
    term = json.loads((ROOT / f"terminal/gruvbox-material-mix-{mode}.json").read_text())["terminal"]
    syntax = {rule["name"]: rule["settings"] for rule in theme["tokenColors"]}
    return theme["tokens"], syntax, term


def window(mode: str, title: str, style: str) -> str:
    t, syntax, term = load(mode)
    tree = "".join(
        f'<div class="row{" sel" if sel else ""}" style="padding-left:{12 + depth * 14}px">'
        f'<span class="dot" style="background:{t["--muted-foreground"]}"></span>{html.escape(name)}</div>'
        for depth, name, sel in TREE
    )
    lines = []
    for n, parts in enumerate(CODE, 1):
        spans = []
        for kind, text in parts:
            if kind == "plain":
                spans.append(html.escape(text))
                continue
            s = syntax[SCOPES[kind]]
            italic = "font-style:italic;" if "italic" in (s.get("fontStyle") or "") else ""
            spans.append(f'<span style="color:{s["foreground"]};{italic}">{html.escape(text)}</span>')
        lines.append(f'<div class="ln"><span class="no" style="color:{t["--muted-foreground"]}">{n}</span>{"".join(spans)}</div>')
    swatches = "".join(
        f'<span style="background:{term[k]}"></span>'
        for k in ("background", "foreground", "red", "yellow", "green", "cyan", "blue", "magenta", "brightBlack")
    )
    terminal = (
        f'<div><span style="color:{term["blue"]}">~/atlas</span> <span style="color:{term["magenta"]}">main</span></div>'
        f'<div><span style="color:{term["green"]}">\u276f</span> git status --short'
        f'<span style="color:{term["brightBlack"]}"> --branch</span></div>'
        f'<div><span style="color:{term["yellow"]}"> M</span> src/theme.ts</div>'
        f'<div><span style="color:{term["red"]}"> D</span> src/palette.ts</div>'
        f'<div><span style="color:{term["green"]}">\u276f</span> <span class="cursor" style="background:{term["cursor"]}"></span></div>'
    )
    return f"""
<div class="win" style="{style};background:{t['--background']};color:{t['--foreground']};border-color:{t['--border']}">
  <div class="bar" style="border-color:{t['--border']}">
    <span class="lights"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i></span>
    <span>atlas \u2014 Orca</span><span class="name" style="color:{t['--muted-foreground']}">{title}</span>
  </div>
  <div class="body">
    <div class="side" style="border-color:{t['--worktree-sidebar-border']};--sel:{t['--sidebar-accent']}">
      <div class="head" style="color:{t['--muted-foreground']}">EXPLORER</div>{tree}
      <div class="badge" style="background:{t['--muted']};color:{t['--muted-foreground']}">BETA</div>
    </div>
    <div class="main">
      <div class="tabs" style="border-color:{t['--border']};background:{t['--tab-bar']}">
        <span class="tab on" style="background:{t['--tab-active']};color:{t['--tab-active-foreground']};border-color:{t['--border']};box-shadow:inset 0 -2px 0 {t['--tab-active-indicator']}">theme.ts</span>
        <span class="tab" style="background:{t['--tab-inactive']};color:{t['--tab-inactive-foreground']};border-color:{t['--border']}">router.ts</span>
        <span class="tab" style="background:{t['--tab-inactive']};color:{t['--tab-inactive-foreground']};border-color:{t['--border']}">README.md</span>
      </div>
      <div class="code">{''.join(lines)}</div>
      <div class="term" style="border-color:{t['--border']}">
        <div class="thead" style="color:{t['--muted-foreground']}">TERMINAL&nbsp;&nbsp;&nbsp;zsh \u2014 atlas</div>
        <div class="tbody" style="color:{term['foreground']}">{terminal}</div>
        <div class="swatches">{swatches}</div>
      </div>
    </div>
  </div>
</div>"""


def page() -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
body {{ margin:0; width:{WIDTH}px; height:{HEIGHT}px; overflow:hidden; font:13px -apple-system, "Helvetica Neue", sans-serif;
  background: linear-gradient(135deg, #282828 0%, #7c6f64 55%, #f4e8be 100%); position:relative; }}
.win {{ position:absolute; width:800px; height:556px; border:1px solid; border-radius:10px; overflow:hidden; box-shadow:0 24px 60px rgba(0,0,0,.35); display:flex; flex-direction:column; }}
.bar {{ height:30px; display:flex; align-items:center; gap:12px; padding:0 12px; font-size:11px; border-bottom:1px solid; }}
.bar .name {{ margin-left:auto; }}
.lights i {{ display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }}
.body {{ flex:1; display:flex; min-height:0; }}
.side {{ width:160px; border-right:1px solid; font-size:11px; padding-top:8px; position:relative; }}
.head {{ font-size:10px; font-weight:600; letter-spacing:.06em; padding:4px 12px 8px; }}
.row {{ height:19px; line-height:19px; margin:0 6px; border-radius:4px; }}
.row.sel {{ background:var(--sel); }}
.dot {{ display:inline-block; width:4px; height:4px; margin-right:8px; vertical-align:middle; opacity:.7; }}
.badge {{ position:absolute; left:12px; bottom:14px; font-size:9px; font-weight:600; letter-spacing:.08em; padding:3px 7px; border-radius:999px; }}
.main {{ flex:1; display:flex; flex-direction:column; min-width:0; }}
.tabs {{ height:28px; display:flex; border-bottom:1px solid; font-size:11px; }}
.tab {{ padding:0 14px; line-height:28px; border-right:1px solid; }}
.code {{ flex:1; padding:12px 0; font:12.5px/17.5px "SF Mono", Menlo, monospace; white-space:pre; }}
.ln .no {{ display:inline-block; width:34px; text-align:right; margin-right:16px; }}
.term {{ height:190px; border-top:1px solid; position:relative; font:12.5px/17.5px "SF Mono", Menlo, monospace; }}
.thead {{ font:10px -apple-system, sans-serif; padding:8px 14px; }}
.tbody {{ padding:4px 16px; white-space:pre; }}
.cursor {{ display:inline-block; width:7px; height:14px; vertical-align:-2px; }}
.swatches {{ position:absolute; right:14px; bottom:14px; display:flex; border-radius:3px; overflow:hidden; }}
.swatches span {{ width:24px; height:18px; }}
</style></head><body>
{window("dark", "Gruvbox Material Mix Dark", "left:70px;top:88px")}
{window("light", "Gruvbox Material Mix Light", "left:730px;top:356px")}
</body></html>"""


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "cover.html"
        source.write_text(page())
        out = ROOT / "images/cover.png"
        subprocess.run(
            [CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=1",
             f"--window-size={WIDTH},{HEIGHT}", f"--screenshot={out}", source.as_uri()],
            check=True,
            capture_output=True,
        )
    print(out)


if __name__ == "__main__":
    main()
