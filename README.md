# Gruvbox Material Mix

> [!IMPORTANT]
> This plugin is no longer maintained and this repository is archived. Its successor,
> [fang2hou/orca-gruvbox-material-theme](https://github.com/fang2hou/orca-gruvbox-material-theme)
> (`fang2hou.gruvbox-material-theme`), ships this Mix Medium variant as
> **Gruvbox Material Dark (Medium, Mix)** and **Gruvbox Material Light (Medium, Mix)**, plus every
> other Gruvbox Material variant:
>
> ```sh
> orca plugin install fang2hou/orca-gruvbox-material-theme
> ```

An Orca port of [sainnhe/gruvbox-material](https://github.com/sainnhe/gruvbox-material)
with `foreground = 'mix'` and `background = 'medium'`: dark and light application
themes with matching syntax and terminal colors. Every color is taken from
sainnhe's palette definitions in `autoload/gruvbox_material.vim`; the Orca-specific
work here is deciding which palette role paints which Orca token.

Select **Gruvbox Material Mix Dark** or **Gruvbox Material Mix Light** in
Appearance, and the theme of the same name in terminal settings.

Both themes use uniform panel backgrounds: Dark uses `#282828`, Light uses
`#fbf1c7`. The editor, sidebars, cards, active tab and terminal share that background; the
tab strip sits one step below it.
Menus and dialogs sit one step above it.

## Installation

The plugin requires Orca **1.4.245 or newer**.

```sh
orca plugin install fang2hou/orca-gruvbox-material-mix-theme
```

## Development and releases

This repository contains one content-only plugin, with its manifest at the root.
No build or dependency installation is needed.

```sh
orca plugin validate .
```

Before publishing a release, update `version` in `orca-plugin.json`, commit the
plugin changes, and push a matching annotated `vX.Y.Z` tag. Installed copies
update with `orca plugin update fang2hou.gruvbox-material-mix-theme`.

## Palette mapping

| Orca role | Palette role |
| --- | --- |
| App, editor, sidebars, cards and the active tab | `bg0` |
| Tab strip and inactive tabs | `bg_dim` (recessed, so the active tab opens into the editor) |
| Menus, popovers and dialogs | `bg1` |
| Secondary and muted fills (badges, chips, tracks) | Dark: `bg_current_word`; Light: `bg4` |
| Sidebar hover and selected rows, terminal selection | `bg3` (the plugin's default `Visual`) |
| Ghost-button and menu hover, selected fills | Dark: `bg3`; Light: `bg5` (stays visible on Orca's tinted sidebar) |
| Main text | `fg0` |
| Muted text | `grey2` nudged toward `fg0` (see below) |
| Inputs | Dark: `bg1`; Light: `bg3` |
| Panel borders and split dividers | Dark: `bg3`; Light: `bg5` |
| Primary action, focus ring, active tab line | `green` (Light button text is white) |
| Links | `blue` |
| Editor selection | `fg0` at 15% (Dark) / 12% (Light) opacity, close to `bg3` |
| Diff backgrounds | `bg_diff_green` / `bg_diff_red` |
| Diff and git decorations | `green` added, `aqua` untracked/copied, `yellow` modified, `red` deleted, `blue` renamed, `grey1` ignored |
| Charts | `green`, `orange`, `blue`, `purple`, `yellow` |

Red stays reserved for deletions and errors, so the accent is green. Light `green`
(`#72761e`) reaches only 4.28:1 against `bg0`, below Orca's 4.5:1 floor for
primary buttons, so Light button text is white (4.85:1) rather than `bg0`.

Orca's **Tinted** left-sidebar mode recomputes the sidebar tokens itself but
still paints ghost buttons (such as Settings' **Back to app**) with `--accent`.
With the default tint, the Light sidebar becomes `#e9e0b9`, which matched the old
`bg3` accent, so Light uses the darker `bg5` for `--accent`.

Muted and secondary fills are deliberately not `bg0`: Orca paints badges (for
example the settings `Beta` tag), keyboard hints and progress tracks with them,
and a `bg0` fill made those shapes disappear. Muted text is nudged toward `fg0`
(Dark `#bbaa90`, Light `#64554a`) so it keeps Orca's 4.5:1 text contrast on every
surface it sits on, hover rows included. Syntax colors meet Orca's 3:1 syntax
contrast floor on the editor background.

The syntax mapping uses red keywords, orange storage modifiers, operators and
tags, green strings and functions, yellow types and escapes, purple booleans,
numbers and decorators, aqua constants, blue variables and links, and italic
`grey1` comments.

Boolean rules target `constant.language.boolean`, `constant.language.true`, and
`constant.language.false`; storage modifiers use `storage.modifier`. Their
appearance depends on the scopes exposed by each language tokenizer.

Terminal colors follow sainnhe's terminal mapping: black is Dark `bg5` / Light
`fg0`, white is Dark `fg0` / Light `bg5`, cyan is `aqua`, and bright colors equal
the normal ones. The one exception is bright black, which is `grey1`
(`#928374`) in both appearances: shells and CLIs draw dimmed text
(autosuggestions, hints, comments) with it, and the upstream value made that
text identical to the foreground in Light.

## Attribution

Gruvbox Material is MIT licensed, Copyright (c) 2020 sainnhe. The Orca token and
TextMate scope mapping started from
[piter75/orca-gruvbox-material-theme](https://github.com/piter75/orca-gruvbox-material-theme)
(MIT, Copyright (c) 2026 Lovecast Inc.), and the panel layout from
[sainnhe/gruvbox-material-vscode](https://github.com/sainnhe/gruvbox-material-vscode).
Both notices are included in [LICENSE](LICENSE).

The cover is an illustrative preview rendered from the plugin JSON by
`scripts/render-cover.py` (needs Google Chrome), rather than a captured Orca
session. Re-run it after changing colors.
