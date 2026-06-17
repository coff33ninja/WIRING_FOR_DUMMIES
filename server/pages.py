"""Page handlers — index, component, fundamental, project, search, missed."""

import re
from pathlib import Path

from .config import DIR
from .markdown import AUTO_LINKS, md_to_html
from .templates import (
    _get_description,
    _get_title,
    build_guide_index,
    build_toc,
    get_headings,
    make_breadcrumbs,
    render_page,
)


def _get_all_content():
    index = []
    for category, cat_label, cat_dir in [
        ("fundamental", "fundamentals", Path(DIR) / "fundamentals"),
        ("component", "components", Path(DIR) / "components"),
        ("project", "projects", Path(DIR) / "projects"),
    ]:
        if cat_dir.exists():
            for f in sorted(cat_dir.iterdir()):
                if f.suffix == ".md":
                    txt = f.read_text("utf-8", errors="replace")
                    title = _get_title(f) or f.stem.replace("-", " ").title()
                    index.append({
                        "type": category,
                        "label": cat_label,
                        "title": title,
                        "slug": f.stem,
                        "text": txt,
                    })
    return index



def highlight_match(text, query):
    i = text.lower().find(query.lower())
    if i < 0:
        return text
    return (
        text[:i]
        + f'<span class="search-highlight">{text[i:i+len(query)]}</span>'
        + text[i+len(query):]
    )



def _build_readme_tables():
    sections = (
        ("fundamentals", "Fundamentals — Start Here",
         "New to electronics? These explain the fundamental concepts you need before wiring anything."),
        ("components", "Component References",
         "These explain what each component *actually does* — read these after the Fundamentals if you need a specific part explained."),
        ("projects", "Project Guides",
         "Complete wiring guides that reference the component explanations above."),
    )
    out = []
    for dirname, heading, intro in sections:
        out.append(f"\n## {heading}\n\n{intro}\n\n| Guide | What it covers |\n|-------|---------------|\n")
        d = Path(DIR) / dirname
        if d.exists():
            for f in sorted(d.iterdir()):
                if f.suffix != ".md":
                    continue
                title = _get_title(f) or f.stem.replace("-", " ").title()
                title_short = title.split(" — ")[0] if "—" in title else title
                desc = _get_description(f)
                if len(desc) > 100:
                    desc = desc[:97] + "..."
                out.append(f"| [{title_short}]({dirname}/{f.stem}.md) | {desc} |\n")
    return "".join(out)



def serve_index():
    path = Path(DIR) / "README.md"
    if not path.exists():
        return build_guide_index()
    md = path.read_text("utf-8", errors="replace")
    start_tag = "<!-- GUIDES:START -->"
    end_tag = "<!-- GUIDES:END -->"
    start_pos = md.find(start_tag)
    end_pos = md.find(end_tag)
    if start_pos != -1 and end_pos != -1:
        md = md[:start_pos + len(start_tag)] + "\n" + _build_readme_tables() + "\n" + md[end_pos:]
    html = md_to_html(md)
    title = "Wiring for Dummies — Guide Index"
    content = f"<h2>{title}</h2>\n{html}"
    return render_page(title, content, "/")



def serve_index_page():
    return build_guide_index()



def serve_search(query):
    if not query:
        return serve_index()
    all_content = _get_all_content()
    q = query.lower()
    results = []
    for item in all_content:
        text_lower = item["text"].lower()
        if q in text_lower:
            context_lines = []
            for line in item["text"].split("\n"):
                if q in line.lower():
                    context_lines.append(line.strip()[:120])
            results.append({**item, "context": context_lines})

    if not results:
        content = f"""
        <h2>Search: "{query}"</h2>
        <p style="color:var(--text-dim);font-size:14px;">No results found for "<strong>{query}</strong>".</p>
        """
        return render_page(f"Search: {query}", content, "/search", search_query=query,
                           breadcrumbs=make_breadcrumbs([("Search", "search")]))

    content = f"""
    <h2>Search: "{query}"</h2>
    <p style="font-size:13px;color:var(--text-dim);margin-bottom:16px;">{len(results)} result{'s' if len(results)!=1 else ''}</p>
    <ul class="search-results">
    """
    for r in results:
        url = f"/{r['label']}/{r['slug']}"
        badge = {"component": "component", "fundamental": "fundamental", "project": "project"}.get(r["type"], "fundamental")
        label = badge.replace("-", " ")
        ctx = ""
        if r["context"]:
            ctx = '<div class="match-preview">' + "".join(
                f"<div>…{highlight_match(c, q)}…</div>" for c in r["context"][:3]
            ) + "</div>"
        content += f"""
        <li>
          <a href="{url}"><span class="badge badge-{badge}">{label}</span> {r['title']}</a>
          <div class="match-path">{r['label']}/{r['slug']}</div>
          {ctx}
        </li>
        """
    content += "</ul>"
    return render_page(f"Search: {query}", content, "/search", search_query=query,
                       breadcrumbs=make_breadcrumbs([("Search", "search")]))



def serve_missed():
    comp_existing = {f.stem.lower() for f in (Path(DIR) / "components").glob("*.md")}
    fund_existing = {f.stem.lower() for f in (Path(DIR) / "fundamentals").glob("*.md")}
    all_existing = comp_existing | fund_existing
    rows = []
    for slug, display in sorted(set((s, d) for _, s, d, _ in AUTO_LINKS)):
        exists = slug in all_existing
        sources = set()
        for src_dir in ["projects", "fundamentals"]:
            for f in (Path(DIR) / src_dir).glob("*.md"):
                if any(re.search(p, f.read_text("utf-8", errors="replace"), re.IGNORECASE) for p, s, _, _ in AUTO_LINKS if s == slug):
                    sources.add(f"{src_dir}/{f.stem}")
        status = '<span style="color:var(--green)">✓</span>' if exists else '<span style="color:var(--accent2)">✗</span>'
        if slug in comp_existing:
            badge = '<span class="badge badge-component" style="font-size:9px">guide</span>'
        elif slug in fund_existing:
            badge = '<span class="badge badge-fundamental" style="font-size:9px">guide</span>'
        else:
            badge = '<span class="badge badge-project" style="font-size:9px">missing</span>'
        src_list = ", ".join(sorted(sources))[:80] if sources else "<em>not referenced</em>"
        rows.append(f"<tr><td>{status}</td><td>{badge} {display}</td><td style='font-size:12px;color:var(--text-dim)'>{src_list}</td></tr>")
    content = f"""<h2>Component Scanner <span style="font-size:14px;color:var(--text-dim)">— admin / missed</span></h2>
    <p style="font-size:14px;color:var(--text-dim);margin-bottom:16px;">
      Scans project and fundamentals files for component mentions, cross-references against existing guides.
    </p>
    <table>
      <tr><th>Status</th><th>Component</th><th>Referenced in</th></tr>
      {"".join(rows)}
    </table>
    <p style="margin-top:16px;font-size:12px;color:var(--text-dim);">
      <span style="color:var(--green)">✓</span> = guide exists &nbsp;|&nbsp;
      <span style="color:var(--accent2)">✗</span> = no guide yet &nbsp;|&nbsp;
      <span class="badge badge-component">guide</span> = has dedicated guide &nbsp;|&nbsp;
      <span class="badge badge-project">missing</span> = needs one
    </p>"""
    return render_page("Component Scanner — Admin", content, "/missed",
                       breadcrumbs=make_breadcrumbs([("Admin", "missed")]))



def serve_component(name):
    path = Path(DIR) / "components" / f"{name}.md"
    if not path.exists():
        return render_page("Not Found", "<h2>Component not found</h2>")
    md = path.read_text("utf-8", errors="replace")
    html = md_to_html(md)
    headings = get_headings(md)
    toc = build_toc(headings)
    title = _get_title(path) or name.replace("-", " ").title()
    title_clean = re.sub(r"\s*[—–-]\s*(Component Reference|Wiring for Dummies).*", "", title)
    content = f"<h2>{title_clean}</h2>\n{toc}\n{html}"
    return render_page(title, content, f"/components/{name}",
                       breadcrumbs=make_breadcrumbs([("Components", "components"), (title_clean, name)]))



def serve_fundamental(name):
    path = Path(DIR) / "fundamentals" / f"{name}.md"
    if not path.exists():
        return render_page("Not Found", "<h2>Fundamentals guide not found</h2>")
    md = path.read_text("utf-8", errors="replace")
    html = md_to_html(md)
    headings = get_headings(md)
    toc = build_toc(headings)
    title = _get_title(path) or name.replace("-", " ").title()
    content = f"<h2>{title}</h2>\n{toc}\n{html}"
    return render_page(title, content, f"/fundamentals/{name}",
                       breadcrumbs=make_breadcrumbs([("Fundamentals", "fundamentals"), (title, name)]))



def serve_project(name):
    path = Path(DIR) / "projects" / f"{name}.md"
    if not path.exists():
        return render_page("Not Found", "<h2>Project not found</h2>")
    md = path.read_text("utf-8", errors="replace")
    html = md_to_html(md)
    headings = get_headings(md)
    toc = build_toc(headings)
    title = _get_title(path) or name.replace("-", " ").title()
    title_clean = re.sub(r"\s*[—–-]\s*(Wiring for Dummies|Project Guide).*", "", title)
    content = f"<h2>{title_clean}</h2>\n{toc}\n{html}"
    return render_page(title, content, f"/projects/{name}",
                       breadcrumbs=make_breadcrumbs([("Projects", "projects"), (title_clean, name)]))

