"""HTML shell, page renderer, sidebar, cards, breadcrumbs, TOC."""

import re
from pathlib import Path

from .config import DIR


def sidebar_active(path, current):
    return "active" if path == current else ""



def get_headings(md_text):
    headings = []
    for line in md_text.split("\n"):
        m = re.match(r"^(#{2,3})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            anchor = re.sub(r"[^a-zA-Z0-9]+", "-", m.group(2).lower()).strip("-")
            headings.append((level, m.group(2), anchor))
    return headings



def build_toc(headings):
    if not headings:
        return ""
    items = "".join(
        f'<li style="padding-left:{12 * (h[0] - 2)}px"><a href="#{h[2]}">{h[1]}</a></li>'
        for h in headings
    )
    return f'<div class="toc"><h3>On this page</h3><ul>{items}</ul></div>'



HTML_SHELL = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<style>
  :root {{
    --bg: #0d0d0d; --surface: #1a1a1a; --surface2: #242424;
    --border: #333; --accent: #44ddff; --accent2: #ff8800;
    --text: #e0e0e0; --text-dim: #888; --green: #44ff44;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: var(--bg); color: var(--text);
    display: flex; min-height: 100vh;
  }}
  .sidebar {{
    width: 280px; min-width: 280px; background: var(--surface);
    border-right: 1px solid var(--border); height: 100vh;
    position: sticky; top: 0; overflow-y: auto;
    padding: 20px; display: flex; flex-direction: column; gap: 6px;
  }}
  .sidebar h1 {{ font-size: 18px; font-weight: 800; margin-bottom: 4px; }}
  .sidebar h1 span {{ color: var(--accent); }}
  .sidebar .subtitle {{ font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 16px; }}
  .sidebar a {{
    display: block; padding: 8px 12px; border-radius: 6px;
    color: var(--text); text-decoration: none; font-size: 13px;
    transition: all 0.15s; border: 1px solid transparent;
  }}
  .sidebar a:hover {{ background: var(--surface2); border-color: var(--border); }}
  .sidebar a.active {{ background: rgba(68,221,255,0.1); border-color: var(--accent); color: var(--accent); }}
  .sidebar .section {{ font-size: 10px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 2px; margin: 12px 0 4px 12px; }}
  .sidebar .search-input {{
    width: 100%; padding: 8px 12px; background: var(--surface2);
    border: 1px solid var(--border); border-radius: 6px; color: var(--text);
    font-size: 13px; outline: none; margin-bottom: 8px;
  }}
  .sidebar .search-input:focus {{ border-color: var(--accent); }}
  .main {{ flex: 1; padding: 32px 48px; overflow-y: auto; max-width: 960px; }}
  .breadcrumbs {{
    font-size: 12px; color: var(--text-dim); margin-bottom: 16px;
    padding-bottom: 12px; border-bottom: 1px solid var(--border);
  }}
  .breadcrumbs a {{ color: var(--accent); text-decoration: none; }}
  .breadcrumbs a:hover {{ text-decoration: underline; }}
  .breadcrumbs span {{ color: var(--text-dim); }}
  .main h2 {{ font-size: 26px; font-weight: 800; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px solid var(--accent); }}
  .main h3 {{ font-size: 18px; font-weight: 700; margin: 24px 0 12px; color: var(--accent); }}
  .main h4 {{ font-size: 15px; font-weight: 700; margin: 20px 0 8px; }}
  .main p {{ font-size: 14px; line-height: 1.7; margin-bottom: 12px; }}
  .main ul, .main ol {{ margin: 8px 0 12px 24px; font-size: 14px; line-height: 1.6; }}
  .main li {{ margin-bottom: 4px; }}
  .main code {{
    background: var(--surface2); padding: 2px 6px; border-radius: 4px;
    font-size: 13px; color: var(--accent2);
  }}
  .main pre {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 16px; overflow-x: auto;
    margin: 12px 0; font-size: 13px; line-height: 1.5;
  }}
  .main pre code {{ background: none; padding: 0; color: var(--green); }}
  .main blockquote {{
    border-left: 3px solid var(--accent2); padding: 8px 16px;
    margin: 12px 0; background: rgba(255,136,0,0.06);
    border-radius: 0 6px 6px 0; font-size: 14px; color: var(--text-dim);
  }}
  .main hr {{ border: none; border-top: 1px solid var(--border); margin: 24px 0; }}
  .main table {{
    width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 13px;
  }}
  .main th, .main td {{
    border: 1px solid var(--border); padding: 8px 12px; text-align: left;
  }}
  .main th {{ background: var(--surface); color: var(--accent); font-weight: 700; }}
  .main tr:nth-child(even) {{ background: rgba(255,255,255,0.02); }}
  .main img {{ max-width: 100%; border-radius: 6px; margin: 12px 0; }}
  .main .toc {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 16px 20px; margin: 16px 0;
  }}
  .main .toc h3 {{ margin-top: 0; font-size: 14px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; }}
  .main .toc ul {{ list-style: none; margin: 8px 0 0 0; padding: 0; }}
  .main .toc li {{ padding: 2px 0; }}
  .main .toc a {{ color: var(--accent); text-decoration: none; font-size: 13px; }}
  .main .toc a:hover {{ text-decoration: underline; }}
  .card-grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 12px; margin: 16px 0;
  }}
  .card {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 16px; text-decoration: none; color: var(--text);
    transition: all 0.15s; display: block;
  }}
  .card:hover {{ border-color: var(--accent); transform: translateY(-2px); }}
  .card h4 {{ font-size: 14px; font-weight: 700; margin-bottom: 4px; }}
  .card p {{ font-size: 12px; color: var(--text-dim); }}
  .badge {{
    display: inline-block; font-size: 10px; font-weight: 700;
    padding: 2px 8px; border-radius: 10px; text-transform: uppercase;
    letter-spacing: 1px;
  }}
  .badge-fundamental {{ background: rgba(68,221,255,0.15); color: var(--accent); }}
  .badge-component {{ background: rgba(68,255,68,0.15); color: var(--green); }}
  .badge-project {{ background: rgba(255,136,0,0.15); color: var(--accent2); }}
  .search-results {{
    list-style: none; padding: 0; margin: 16px 0;
  }}
  .search-results li {{
    padding: 12px 16px; background: var(--surface); border: 1px solid var(--border);
    border-radius: 6px; margin-bottom: 8px;
  }}
  .search-results li a {{
    color: var(--accent); text-decoration: none; font-weight: 600; font-size: 14px;
  }}
  .search-results li a:hover {{ text-decoration: underline; }}
  .search-results li .match-preview {{
    font-size: 12px; color: var(--text-dim); margin-top: 4px;
  }}
  .search-results li .match-path {{
    font-size: 11px; color: var(--accent2); margin-top: 2px;
  }}
  .search-highlight {{
    background: rgba(255,136,0,0.2); color: var(--accent2); padding: 0 2px;
    border-radius: 2px;
  }}
  ::-webkit-scrollbar {{ width: 6px; }}
  ::-webkit-scrollbar-track {{ background: transparent; }}
  ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}
  @media (max-width: 768px) {{
    body {{ flex-direction: column; }}
    .sidebar {{ width: 100%; min-width: unset; height: auto; max-height: 40vh; position: static; border-right: none; border-bottom: 1px solid var(--border); }}
    .main {{ padding: 20px; }}
  }}
  .toast {{
    position: fixed; bottom: 24px; right: 24px; padding: 12px 20px;
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 8px; font-size: 13px; opacity: 0;
    transform: translateY(20px); transition: all 0.3s; z-index: 999;
    pointer-events: none;
  }}
  .toast.show {{ opacity: 1; transform: translateY(0); }}
  .tabs {{
    display: flex; gap: 4px; margin-bottom: 20px; flex-wrap: wrap;
  }}
  .tab-btn {{
    padding: 8px 20px; background: var(--surface); border: 1px solid var(--border);
    border-radius: 6px; color: var(--text-dim); font-size: 13px;
    cursor: pointer; transition: all 0.15s;
  }}
  .tab-btn:hover {{ border-color: var(--accent); color: var(--text); }}
  .tab-btn.active {{ background: rgba(68,221,255,0.1); border-color: var(--accent); color: var(--accent); font-weight: 600; }}
  .tab-panel {{ display: none; }}
  .tab-panel.active {{ display: block; }}
</style>
</head>
<body>
<nav class="sidebar">
  <h1>WIRING <span>FOR DUMMIES</span></h1>
  <div class="subtitle">Electronics · Hardware · IoT</div>
  <a href="/" class="{home_active}">Home</a>
  <a href="/index" class="{guide_active}">Index</a>
  <form action="/search" method="get" style="margin: 4px 0;">
    <input type="text" name="q" class="search-input" placeholder="Search guides..." value="{search_query}">
  </form>
  <div class="section">Fundamentals</div>
  {fundamental_links}
  <div class="section">Components</div>
  {component_links}
  <div class="section">Projects</div>
  {project_links}
</nav>
<main class="main">
{breadcrumbs}
{content}
</main>
<div class="toast" id="toast"></div>
</body>
</html>"""



def render_page(title, content, current_path="", search_query="", breadcrumbs=""):
    comp_links = ""
    comp_dir = Path(DIR) / "components"
    if comp_dir.exists():
        for f in sorted(comp_dir.iterdir()):
            if f.suffix == ".md":
                name = f.stem.replace("-", " ").title()
                comp_links += f'<a href="/components/{f.stem}">{name}</a>\n'

    fund_links = ""
    fund_dir = Path(DIR) / "fundamentals"
    if fund_dir.exists():
        for f in sorted(fund_dir.iterdir()):
            if f.suffix == ".md":
                name = f.stem.replace("-", " ").title()
                fund_links += f'<a href="/fundamentals/{f.stem}">{name}</a>\n'

    proj_links = ""
    proj_dir = Path(DIR) / "projects"
    if proj_dir.exists():
        for f in sorted(proj_dir.iterdir()):
            if f.suffix == ".md":
                name = f.stem.replace("-", " ").title()
                proj_links += f'<a href="/projects/{f.stem}">{name}</a>\n'

    return HTML_SHELL.format(
        title=title,
        content=content,
        home_active=sidebar_active("/", current_path),
        guide_active=sidebar_active("/guide", current_path),
        fundamental_links=fund_links,
        component_links=comp_links,
        project_links=proj_links,
        breadcrumbs=breadcrumbs,
        search_query=search_query,
    )



def card(title, desc, url, badge):
    display = badge.replace("-", " ")
    return f'<a href="{url}" class="card"><h4><span class="badge badge-{badge}">{display}</span> {title}</h4><p>{desc}</p></a>'



def make_breadcrumbs(parts):
    crumbs = '<a href="/">Home</a>'
    path = ""
    for label, slug in parts:
        path += f"/{slug}"
        if slug == parts[-1][1]:
            crumbs += f" <span>›</span> <span>{label}</span>"
        else:
            crumbs += f' <span>›</span> <a href="{path}">{label}</a>'
    return f'<div class="breadcrumbs">{crumbs}</div>'



def build_guide_index():
    sections = (
        ("fundamentals", "Fundamentals", "fundamental"),
        ("components", "Components", "component"),
        ("projects", "Projects", "project"),
    )
    tab_cards = []
    tab_buttons = ""
    tab_panels = ""
    first = True
    for dirname, label, badge in sections:
        d = Path(DIR) / dirname
        cards = []
        if d.exists():
            for f in sorted(d.iterdir()):
                if f.suffix != ".md":
                    continue
                title = _get_title(f) or f.stem.replace("-", " ").title()
                title_short = title.split(" — ")[0] if "—" in title else title
                desc = _get_description(f)
                cards.append(card(title_short, desc, f"{dirname}/{f.stem}", badge))
        active = " active" if first else ""
        tab_buttons += f'<button class="tab-btn{active}" onclick="switchTab(this,\'{dirname}\')">{label} ({len(cards)})</button>\n'
        tab_panels += f'<div id="tab-{dirname}" class="tab-panel{active}"><div class="card-grid">{"".join(cards)}</div></div>\n'
        tab_cards.append(cards)
        first = False
    content = f"""<h2>Index</h2>
    <p style="font-size:14px;color:var(--text-dim);margin-bottom:24px;">
      Electronics reference guides — from basic components to complete IoT projects.
      Each guide explains <em>why</em> every wire and part is there, not just where it goes.
    </p>
    <div class="tabs">
      {tab_buttons.strip()}
    </div>
    {tab_panels.strip()}
    <script>
    function switchTab(btn,name){{document.querySelectorAll('.tab-btn').forEach(function(b){{b.classList.remove('active')}});document.querySelectorAll('.tab-panel').forEach(function(p){{p.classList.remove('active')}});btn.classList.add('active');document.getElementById('tab-'+name).classList.add('active')}}
    </script>"""
    return render_page("Index", content, "/index",
                       breadcrumbs=make_breadcrumbs([("Index", "index")]))



def _get_title(path):
    try:
        txt = Path(path).read_text("utf-8", errors="replace")
        m = re.search(r"^#\s+(.+)$", txt, re.MULTILINE)
        return m.group(1) if m else None
    except:
        return None



def _get_description(path):
    try:
        txt = Path(path).read_text("utf-8", errors="replace")
    except:
        return ""
    lines = txt.split("\n")
    found_h1 = False
    desc_lines = []
    for line in lines:
        if not found_h1:
            if line.startswith("# ") and not line.startswith("## "):
                found_h1 = True
            continue
        if not line.strip() or line.startswith("#") or line.startswith("```"):
            if desc_lines:
                break
            continue
        if line.strip() in ("---", "***", "___"):
            continue
        desc_lines.append(line.strip())
    desc = " ".join(desc_lines)
    desc = re.sub(r"\*\*(.+?)\*\*", r"\1", desc)
    desc = re.sub(r"__(.+?)__", r"\1", desc)
    desc = re.sub(r"\*(.+?)\*", r"\1", desc)
    desc = re.sub(r"_(.+?)_", r"\1", desc)
    desc = re.sub(r"`(.+?)`", r"\1", desc)
    if len(desc) > 150:
        desc = desc[:147] + "..."
    return desc

