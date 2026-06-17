#!/usr/bin/env python3
"""Split the original monolithic serve.py into server/ modules + main.py entry point.

Reads serve.py from the working directory and writes:
  server/__init__.py
  server/config.py         — PORT, DIR, MIME, self_ip()
  server/markdown.py       — html_escape(), inline(), AUTO_LINKS, auto_link(), md_to_html()
  server/templates.py      — HTML_SHELL, sidebar_active(), get_headings(), build_toc(),
                             render_page(), card(), make_breadcrumbs(), build_guide_index(),
                             _get_title(), _get_description()
  server/pages.py          — _get_all_content(), serve_search(), serve_missed(),
                             highlight_match(), _build_readme_tables(), serve_index(),
                             serve_index_page(), serve_component(), serve_project(),
                             serve_fundamental()
  main.py                  — Handler class + startup (imports from server.*)
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVE_PATH = ROOT / "serve.py"
SERVER_DIR = ROOT / "server"


def lines_to_text(lines):
    return "".join(lines)


# ── Read original serve.py ────────────────────────────────────
src = SERVE_PATH.read_text("utf-8")
lines = src.split("\n")
# preserve line endings
src_lines = [line + "\n" for line in lines]
# last line might not have newline
src_lines[-1] = lines[-1]

# ── Section definitions: (name, start_line_0idx, end_line_0idx_exclusive) ──
# These match the original file layout. Update if serve.py changes.
sections = {
    "imports":         (0, 11),       # #!/usr/bin + imports
    "config":          (11, 36),      # PORT, DIR, MIME, self_ip()
    "md_to_html":      (38, 139),     # md_to_html()
    "inline":          (139, 151),    # inline()
    "html_escape":     (151, 155),    # html_escape()
    "AUTO_LINKS":      (155, 322),    # AUTO_LINKS list + sort
    "auto_link":       (322, 352),    # auto_link()
    "HTML_SHELL":      (352, 538),    # HTML_SHELL template
    "sidebar_active":  (538, 542),    # sidebar_active()
    "get_headings":    (542, 553),    # get_headings()
    "build_toc":       (553, 563),    # build_toc()
    "render_page":     (563, 601),    # render_page()
    "card":            (601, 606),    # card()
    "make_breadcrumbs":(606, 618),    # make_breadcrumbs()
    "build_guide_index":(618, 660),   # build_guide_index()
    "get_title":       (660, 669),    # _get_title()
    "get_description": (669, 700),    # _get_description()
    "get_all_content": (700, 722),    # _get_all_content()
    "serve_search":    (722, 771),    # serve_search()
    "serve_missed":    (771, 810),    # serve_missed()
    "highlight_match": (810, 821),    # highlight_match()
    "build_readme_tables": (821, 847), # _build_readme_tables()
    "serve_index":     (847, 864),    # serve_index()
    "serve_index_page":(864, 868),    # serve_index_page()
    "serve_component": (868, 883),    # serve_component()
    "serve_project":   (883, 898),    # serve_project()
    "serve_fundamental":(898, 912),   # serve_fundamental()
    "Handler":         (912, 969),    # Handler class
    "startup":         (969, 990),    # print + server startup
}

def get_section(name):
    start, end = sections[name]
    return "".join(src_lines[start:end])


# ── Module writers ────────────────────────────────────────────

def write_init():
    (SERVER_DIR / "__init__.py").write_text("")
    print("  server/__init__.py")

def write_config():
    parts = [
        '"""Configuration — port, paths, MIME types, network IP."""\n',
        "\n",
        get_section("imports"),
        "\n",
        get_section("config"),
    ]
    text = "".join(parts)
    # Keep imports local; strip the shebang
    text = text.replace("#!/usr/bin/env python3\n", "")
    (SERVER_DIR / "config.py").write_text(text)
    print("  server/config.py")

def write_markdown():
    parts = [
        '"""Markdown-to-HTML renderer with auto-linking."""\n',
        "\n",
        "import re\n",
        "\n",
        get_section("html_escape"),
        "\n",
        get_section("AUTO_LINKS"),
        "\n",
        get_section("auto_link"),
        "\n",
        # inline() needs html_escape + auto_link — both above
        get_section("inline"),
        "\n",
        get_section("md_to_html"),
    ]
    text = "".join(parts)
    text = text.replace("#!/usr/bin/env python3\n", "")
    # inline() uses auto_link which is defined above — good
    (SERVER_DIR / "markdown.py").write_text(text)
    print("  server/markdown.py")

def write_templates():
    parts = [
        '"""HTML shell, page renderer, sidebar, cards, breadcrumbs, TOC."""\n',
        "\n",
        "import re\n",
        "from pathlib import Path\n",
        "from .config import DIR\n",
        "\n",
        get_section("sidebar_active"),
        "\n",
        get_section("get_headings"),
        "\n",
        get_section("build_toc"),
        "\n",
        get_section("HTML_SHELL"),
        "\n",
        get_section("render_page"),
        "\n",
        get_section("card"),
        "\n",
        get_section("make_breadcrumbs"),
        "\n",
        get_section("build_guide_index"),
        "\n",
        get_section("get_title"),
        "\n",
        get_section("get_description"),
    ]
    text = "".join(parts)
    text = text.replace("#!/usr/bin/env python3\n", "")
    # fix _get_title signature — original takes a Path, keep as-is
    # fix DIR reference — uses module-level DIR from .config
    (SERVER_DIR / "templates.py").write_text(text)
    print("  server/templates.py")

def write_pages():
    parts = [
        '"""Page handlers — index, component, fundamental, project, search, missed."""\n',
        "\n",
        "import re\n",
        "from pathlib import Path\n",
        "from .config import DIR\n",
        "from .markdown import md_to_html\n",
        "from .templates import (\n",
        "    render_page, card, make_breadcrumbs, build_guide_index,\n",
        "    build_toc, _get_title, _get_description, sidebar_active,\n",
        ")\n",
        "from .markdown import AUTO_LINKS\n",
        "\n",
        get_section("get_all_content"),
        "\n",
        get_section("highlight_match"),
        "\n",
        get_section("build_readme_tables"),
        "\n",
        get_section("serve_index"),
        "\n",
        get_section("serve_index_page"),
        "\n",
        get_section("serve_search"),
        "\n",
        get_section("serve_missed"),
        "\n",
        get_section("serve_component"),
        "\n",
        get_section("serve_fundamental"),
        "\n",
        get_section("serve_project"),
    ]
    text = "".join(parts)
    text = text.replace("#!/usr/bin/env python3\n", "")
    (SERVER_DIR / "pages.py").write_text(text)
    print("  server/pages.py")

def write_main():
    parts = [
        "#!/usr/bin/env python3\n",
        '"""Documentation server for Wiring for Dummies — entry point."""\n',
        "\n",
        "import http.server\n",
        "import webbrowser\n",
        "import urllib.parse\n",
        "from pathlib import Path\n",
        "from server.config import PORT, DIR, MIME, self_ip\n",
        "from server.pages import (\n",
        "    serve_index, serve_index_page, serve_missed,\n",
        "    serve_component, serve_fundamental, serve_project,\n",
        "    serve_search,\n",
        ")\n",
        "\n",
        get_section("Handler"),
        "\n",
        "def main():\n",
    ]
    # startup lines (971-989) need to be indented under def main():
    startup = get_section("startup")
    # indent each non-empty line under main()
    indented = []
    for line in startup.split("\n"):
        stripped = line.strip()
        if not stripped:
            indented.append("")
        elif stripped == "try:":
            indented.append("    try:")
        elif stripped in ("except OSError:", "except KeyboardInterrupt:"):
            indented.append(f"    {stripped}")
        else:
            indented.append(f"    {line}")
    startup_indented = "\n".join(indented)

    # Also add the shebang-protected lines under main()
    parts.append(startup_indented)
    parts.append("\n\n")
    parts.append('if __name__ == "__main__":\n')
    parts.append("    main()\n")

    text = "".join(parts)
    # The lines from get_section already have newlines
    (ROOT / "main.py").write_text(text)
    print("  main.py")


# ── Run ───────────────────────────────────────────────────────
SERVER_DIR.mkdir(parents=True, exist_ok=True)

write_init()
write_config()
write_markdown()
write_templates()
write_pages()
write_main()

print("\n  Done. Run: python main.py")
