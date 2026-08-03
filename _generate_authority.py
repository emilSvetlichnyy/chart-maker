#!/usr/bin/env python3
"""Generate Learn/Compare pillars and patch sitewide IA from knowledge-graph.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KG = json.loads((ROOT / "knowledge-graph.json").read_text())
BASE = KG["product"]["siteBase"]
APP = KG["product"]["appStoreUrl"]
TYPES_LABEL = "pie, donut, line, area, bar, H. Bar, stacked, scatter, radar, and gantt"

ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "VIA",
    "alternateName": "VIA Chart Builder",
    "url": f"{BASE}/",
    "logo": f"{BASE}/apple-touch-icon.png",
    "description": f"VIA is a native iOS chart maker for {TYPES_LABEL} charts.",
    "sameAs": [APP, KG["product"]["developerUrl"]],
    "founder": {
        "@type": "Person",
        "name": KG["product"]["developer"],
        "url": KG["product"]["developerUrl"],
    },
}


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def jd(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


def prefix_for(rel_dir: Path) -> str:
    depth = len(rel_dir.parts)
    return "../" * depth if depth else "./"


def nav_html(prefix: str, current: str | None = None) -> str:
    items = [
        ("Types", f"{prefix}chart-types/", "Types"),
        ("Compare", f"{prefix}compare/", "Compare"),
        ("Learn", f"{prefix}learn/", "Learn"),
        ("Tools", f"{prefix}tools/", "Tools"),
    ]
    links = []
    for label, href, key in items:
        cur = ' aria-current="page"' if current == key else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    return (
        f'<nav class="nav-links" aria-label="Sections">\n'
        + "\n".join(f"        {l}" for l in links)
        + "\n      </nav>"
    )


def crumbs_html(items: list[tuple[str, str | None]]) -> str:
    parts = []
    for i, (name, href) in enumerate(items):
        if i:
            parts.append('<span class="crumb-sep" aria-hidden="true">›</span>')
        if href and i < len(items) - 1:
            parts.append(f'<a href="{href}">{esc(name)}</a>')
        else:
            parts.append(f'<span aria-current="page">{esc(name)}</span>')
    return (
        '<nav class="breadcrumbs" aria-label="Breadcrumb">'
        + "".join(parts)
        + "</nav>"
    )


def breadcrumb_ld(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": url,
            }
            for i, (name, url) in enumerate(items)
        ],
    }


def faq_ld(pairs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in pairs
        ],
    }


def article_ld(headline: str, description: str, url: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": description,
        "author": {
            "@type": "Person",
            "name": KG["product"]["developer"],
            "url": KG["product"]["developerUrl"],
        },
        "publisher": {
            "@type": "Organization",
            "name": "VIA",
            "logo": {"@type": "ImageObject", "url": f"{BASE}/apple-touch-icon.png"},
        },
        "mainEntityOfPage": url,
        "dateModified": KG["verifiedAt"],
    }


def soft_cta(prefix: str) -> str:
    return f"""      <section class="section cta-band">
        <div class="section-head"><h2>Build it on iPhone</h2></div>
        <p class="lead-sm">When you want a native editor with ten chart types and PNG/JPEG/PDF export, open VIA. Re-enter values in the app — there is no automatic browser handoff.</p>
        <div class="actions">
          <a class="appstore" href="{APP}" target="_blank" rel="noopener noreferrer" aria-label="Download on the App Store">
            <svg class="appstore__icon" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.365 12.195c-.014-2.09 1.71-3.1 1.783-3.145-.972-1.422-2.48-1.616-3.012-1.64-1.28-.13-2.497.744-3.146.744-.648 0-1.65-.725-2.715-.705-1.396.02-2.69.813-3.41 2.06-1.458 2.53-.371 6.266 1.05 8.312.71 1.02 1.55 2.17 2.65 2.13 1.07-.04 1.47-.69 2.76-.69s1.65.69 2.78.67c1.15-.02 1.88-1.04 2.59-2.06.81-1.18 1.15-2.32 1.16-2.38-.025-.01-2.23-.855-2.49-2.296zM13.64 5.885c.57-.69.955-1.65.85-2.6-.82.03-1.81.545-2.4 1.235-.53.615-.996 1.596-.87 2.54.92.07 1.86-.47 2.42-1.175z"/></svg>
            <span class="appstore__text"><span class="appstore__small">Download on the</span><span class="appstore__big">App Store</span></span>
          </a>
          <a class="btn btn-secondary" href="{prefix}chart-types/">All chart types</a>
        </div>
      </section>"""


def page_shell(
    *,
    title: str,
    description: str,
    canonical: str,
    og_image: str,
    prefix: str,
    nav_current: str | None,
    crumbs: list[tuple[str, str | None]],
    crumb_ld_items: list[tuple[str, str]],
    schemas: list[dict],
    body: str,
    brand_href: str | None = None,
) -> str:
    brand = brand_href or f"{prefix}"
    if brand == "./":
        brand = "./"
    schemas_html = "\n".join(
        f'  <script type="application/ld+json">\n{jd(s)}\n  </script>'
        for s in [ORG, breadcrumb_ld(crumb_ld_items), *schemas]
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#0f766e">
  <link rel="icon" href="/chart-maker/favicon.ico">
  <link rel="apple-touch-icon" href="/chart-maker/apple-touch-icon.png">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-title" content="VIA">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="VIA">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{og_image}">
  <link rel="alternate" type="application/rss+xml" title="VIA Chart Guides" href="{BASE}/feed.xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,550;9..40,650;9..40,700&family=Fraunces:opsz,wght@9..144,550;9..144,650&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}styles.css">
{schemas_html}
</head>
<body>
  <div class="wrap">
    <header class="site-nav">
      <a class="brand" href="{brand}">VIA <small>chart maker</small></a>
      {nav_html(prefix, nav_current)}
    </header>
    {crumbs_html(crumbs)}
    <main>
{body}
    </main>
    <footer class="site-footer">
      <a href="{prefix}">← Home</a>
      <a href="{APP}">App Store</a>
    </footer>
  </div>
</body>
</html>
"""


def entity(eid: str) -> dict:
    return KG["entities"][eid]


def slug_href(prefix: str, slug: str) -> str:
    return f"{prefix}{slug}/"


def comparison_page(comp: dict) -> None:
    a, b = entity(comp["a"]), entity(comp["b"])
    slug = comp["slug"]
    rel = Path("compare") / slug
    prefix = "../../"
    url = f"{BASE}/compare/{slug}/"
    desc = comp["quickAnswer"][:158]
    if len(desc) < 140:
        desc = (comp["quickAnswer"] + " Educational guide from VIA.")[:158]

    header, *rows = comp["table"]
    table_rows = "".join(
        "<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>" for row in rows
    )
    table_head = "".join(f"<th>{esc(c)}</th>" for c in header)

    faqs = [
        (f"{a['label']} or {b['label']}?", comp["quickAnswer"]),
        ("Decision rule?", comp["decisionRule"]),
        (
            "Does VIA support both?",
            f"Yes. VIA includes {a.get('uiLabel', a['label'])} and {b.get('uiLabel', b['label'])}. "
            + (
                "Export for Pro-gated types requires VIA Pro."
                if a.get("requiresProExport") or b.get("requiresProExport")
                else "Both export on the free tier."
            ),
        ),
        (
            "Is there a live browser tool?",
            "This site’s live makers cover pie and bar only. Other types are built in the VIA iPhone app.",
        ),
    ]

    related = f"""
      <section class="section">
        <div class="section-head"><h2>Related</h2></div>
        <div class="hub-grid">
          <a class="hub-link" href="{prefix}{a['slug']}/">{esc(a['label'])} chart <span>→</span></a>
          <a class="hub-link" href="{prefix}{b['slug']}/">{esc(b['label'])} chart <span>→</span></a>
          <a class="hub-link" href="{prefix}learn/choose-a-chart-type/">Choose a chart type <span>→</span></a>
          <a class="hub-link" href="{prefix}compare/">All comparisons <span>→</span></a>
          <a class="hub-link" href="{prefix}chart-types/">Chart types <span>→</span></a>
          <a class="hub-link" href="{prefix}learn/common-chart-mistakes/">Common mistakes <span>→</span></a>
        </div>
      </section>"""

    body = f"""
      <section class="hero">
        <p class="eyebrow">Comparison</p>
        <h1>{esc(comp['title'])}</h1>
        <p class="lead">{esc(comp['quickAnswer'])}</p>
      </section>

      <section class="section prose answer-block">
        <div class="section-head"><h2>Quick answer</h2></div>
        <p class="quick-answer">{esc(comp['quickAnswer'])}</p>
        <p><strong>Decision rule:</strong> {esc(comp['decisionRule'])}</p>
      </section>

      <section class="section">
        <div class="section-head"><h2>Side-by-side</h2></div>
        <div class="table-wrap">
          <table class="compare-table">
            <thead><tr>{table_head}</tr></thead>
            <tbody>{table_rows}</tbody>
          </table>
        </div>
      </section>

      <section class="section prose">
        <div class="section-head"><h2>Definitions</h2></div>
        <p><strong>{esc(a['label'])}:</strong> {esc(a['definition'])}</p>
        <p><strong>{esc(b['label'])}:</strong> {esc(b['definition'])}</p>
      </section>

      <section class="section">
        <div class="section-head"><h2>Common mistakes</h2></div>
        <div class="callouts">
          {''.join(f'<div class="callout">{esc(m)}</div>' for m in (a.get('commonMistakes', []) + b.get('commonMistakes', []))[:4])}
        </div>
      </section>

      <section class="section faq" id="questions">
        <div class="section-head"><h2>FAQ</h2></div>
        {''.join(f'<details{" open" if i==0 else ""}><summary>{esc(q)}</summary><p>{esc(a_)}</p></details>' for i,(q,a_) in enumerate(faqs))}
      </section>
{related}
{soft_cta(prefix)}
"""
    html = page_shell(
        title=f"{comp['title']} — Which Should You Use? | VIA",
        description=desc,
        canonical=url,
        og_image=f"{BASE}/assets/og/graph-maker.png",
        prefix=prefix,
        nav_current="Compare",
        crumbs=[
            ("Home", f"{prefix}"),
            ("Compare", f"{prefix}compare/"),
            (comp["title"], None),
        ],
        crumb_ld_items=[
            ("Home", f"{BASE}/"),
            ("Compare", f"{BASE}/compare/"),
            (comp["title"], url),
        ],
        schemas=[
            article_ld(comp["title"], desc, url),
            faq_ld(faqs),
        ],
        body=body,
    )
    out = ROOT / rel / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("wrote", out.relative_to(ROOT))


def write_learn_hub() -> None:
    prefix = "../"
    url = f"{BASE}/learn/"
    desc = "Learn data visualization: choose a chart type, glossary terms, common mistakes, and chart vs graph — educational guides independent of any one app."
    faqs = [
        ("Is this marketing for VIA?", "Guides are written to stand alone. VIA is mentioned only where it implements the chart type or workflow."),
        ("Where should I start?", "Start with Choose a chart type, then open the matching comparison or type guide."),
        ("Do you cover Excel or Tableau?", "We teach chart choice and literacy. Product-specific Excel/Tableau menus are out of scope; we stay honest about what VIA does and does not do."),
    ]
    body = f"""
      <section class="hero">
        <p class="eyebrow">Education</p>
        <h1>Learn chart design — not app menus.</h1>
        <p class="lead">Decision guides, definitions, and mistakes worth avoiding. Every page should still help if you never install VIA.</p>
      </section>
      <section class="section">
        <div class="section-head"><h2>Start here</h2></div>
        <div class="dir-grid">
          <a class="dir-link" href="./choose-a-chart-type/"><div><strong>Choose a chart type</strong><span>Decision rules</span></div><span class="arrow">→</span></a>
          <a class="dir-link" href="./glossary/"><div><strong>Glossary</strong><span>Chart vocabulary</span></div><span class="arrow">→</span></a>
          <a class="dir-link" href="./common-chart-mistakes/"><div><strong>Common mistakes</strong><span>What breaks clarity</span></div><span class="arrow">→</span></a>
          <a class="dir-link" href="./chart-vs-graph/"><div><strong>Chart vs graph</strong><span>Terminology</span></div><span class="arrow">→</span></a>
          <a class="dir-link" href="../compare/"><div><strong>Comparisons</strong><span>Pie vs bar and more</span></div><span class="arrow">→</span></a>
          <a class="dir-link" href="../chart-types/"><div><strong>All chart types</strong><span>Catalog</span></div><span class="arrow">→</span></a>
        </div>
      </section>
      <section class="section faq" id="questions">
        <div class="section-head"><h2>FAQ</h2></div>
        {''.join(f'<details{" open" if i==0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for i,(q,a) in enumerate(faqs))}
      </section>
{soft_cta(prefix)}
"""
    html = page_shell(
        title="Learn Data Visualization & Chart Design | VIA",
        description=desc[:158],
        canonical=url,
        og_image=f"{BASE}/assets/og/home.png",
        prefix=prefix,
        nav_current="Learn",
        crumbs=[("Home", prefix), ("Learn", None)],
        crumb_ld_items=[("Home", f"{BASE}/"), ("Learn", url)],
        schemas=[article_ld("Learn data visualization", desc, url), faq_ld(faqs)],
        body=body,
    )
    out = ROOT / "learn" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("wrote", out.relative_to(ROOT))


def write_chooser() -> None:
    prefix = "../../"
    url = f"{BASE}/learn/choose-a-chart-type/"
    desc = "Choose the right chart type with clear decision rules: part-to-whole, ranking, trends, relationships, profiles, and timelines — before you open any app."
    entities = [
        e
        for e in KG["entities"].values()
        if e.get("kind") == "chartType"
    ]
    cards = []
    for e in entities:
        use = "; ".join(e.get("whenToUse", [])[:2])
        cards.append(
            f'<article class="prose-card"><h3><a href="{prefix}{e["slug"]}/">{esc(e["label"])}</a></h3>'
            f"<p>{esc(use)}</p></article>"
        )
    faqs = [
        ("How do I choose a chart type?", "Start from the question: part-to-whole, ranking, trend, relationship, profile, or timeline — then pick the matching type."),
        ("Pie or bar?", "Pie for shares of one total with few categories; bar for comparing magnitudes. See the pie vs bar guide."),
        ("What does VIA support?", f"VIA includes {TYPES_LABEL}. Browser tools on this site cover pie and bar only."),
    ]
    body = f"""
      <section class="hero">
        <p class="eyebrow">Decision guide</p>
        <h1>Choose a chart type.</h1>
        <p class="lead">Pick the visual from the question you need answered — not from which icon looks familiar.</p>
      </section>
      <section class="section prose answer-block">
        <div class="section-head"><h2>Quick answer</h2></div>
        <p class="quick-answer">Part-to-whole → pie/donut. Ranking categories → bar or H. Bar. Trend over time → line/area. Two numeric variables → scatter. Multi-attribute profile → radar. Task schedule → gantt.</p>
      </section>
      <section class="section">
        <div class="section-head"><h2>Decision rules</h2></div>
        <div class="callouts">
          <div class="callout"><strong>Parts of one total</strong> — Pie or donut. Keep 3–6 slices. <a href="{prefix}compare/pie-vs-bar/">Pie vs bar</a></div>
          <div class="callout"><strong>Compare / rank categories</strong> — Bar; use <a href="{prefix}horizontal-bar-chart/">H. Bar</a> for long labels.</div>
          <div class="callout"><strong>Change over a sequence</strong> — <a href="{prefix}compare/bar-vs-line/">Line</a>; use area when filled volume helps. <a href="{prefix}compare/line-vs-area/">Line vs area</a></div>
          <div class="callout"><strong>Relationship between two numbers</strong> — Scatter (X and Y).</div>
          <div class="callout"><strong>Profile across attributes</strong> — Radar (also called spider). Prefer bars if exact ranking matters. <a href="{prefix}compare/radar-vs-bar/">Radar vs bar</a></div>
          <div class="callout"><strong>Task dates</strong> — Gantt for start/end timelines.</div>
        </div>
      </section>
      <section class="section prose">
        <div class="section-head"><h2>Types at a glance</h2></div>
        <div class="prose-grid">{''.join(cards)}</div>
      </section>
      <section class="section faq" id="questions">
        <div class="section-head"><h2>FAQ</h2></div>
        {''.join(f'<details{" open" if i==0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for i,(q,a) in enumerate(faqs))}
      </section>
      <section class="section">
        <div class="section-head"><h2>Related</h2></div>
        <div class="hub-grid">
          <a class="hub-link" href="{prefix}compare/">Comparisons <span>→</span></a>
          <a class="hub-link" href="{prefix}learn/common-chart-mistakes/">Common mistakes <span>→</span></a>
          <a class="hub-link" href="{prefix}chart-types/">Chart types <span>→</span></a>
          <a class="hub-link" href="{prefix}learn/glossary/">Glossary <span>→</span></a>
        </div>
      </section>
{soft_cta(prefix)}
"""
    html = page_shell(
        title="Choose a Chart Type — Decision Guide | VIA",
        description=desc[:158],
        canonical=url,
        og_image=f"{BASE}/assets/og/home.png",
        prefix=prefix,
        nav_current="Learn",
        crumbs=[
            ("Home", prefix),
            ("Learn", f"{prefix}learn/"),
            ("Choose a chart type", None),
        ],
        crumb_ld_items=[
            ("Home", f"{BASE}/"),
            ("Learn", f"{BASE}/learn/"),
            ("Choose a chart type", url),
        ],
        schemas=[article_ld("Choose a chart type", desc, url), faq_ld(faqs)],
        body=body,
    )
    out = ROOT / "learn" / "choose-a-chart-type" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("wrote", out.relative_to(ROOT))


def write_glossary() -> None:
    prefix = "../../"
    url = f"{BASE}/learn/glossary/"
    desc = "Chart and data visualization glossary: chart, graph, legend, axis, series, part-to-whole, correlation, baseline, export — clear definitions for students and makers."
    terms = KG["glossary"]
    defined = {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "name": "VIA chart glossary",
        "url": url,
        "hasDefinedTerm": [
            {
                "@type": "DefinedTerm",
                "name": t["term"],
                "description": t["definition"],
                "url": f"{url}#{t['slug']}",
            }
            for t in terms
        ],
    }
    items = "".join(
        f'<article class="glossary-item" id="{esc(t["slug"])}">'
        f"<h3>{esc(t['term'])}</h3><p>{esc(t['definition'])}</p></article>"
        for t in terms
    )
    faqs = [
        ("Chart or graph?", "In everyday data viz, the words are often interchangeable. See the chart vs graph guide."),
        ("Does VIA support multiple series?", "No. VIA uses a single flat series of points. Documented as a product limit."),
        ("Where are chart type definitions?", "Each type page and the chart types hub."),
    ]
    body = f"""
      <section class="hero">
        <p class="eyebrow">Glossary</p>
        <h1>Chart vocabulary, defined.</h1>
        <p class="lead">Short definitions you can cite. Product limits are stated when a term maps to VIA behavior.</p>
      </section>
      <section class="section glossary-list">{items}</section>
      <section class="section faq" id="questions">
        <div class="section-head"><h2>FAQ</h2></div>
        {''.join(f'<details{" open" if i==0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for i,(q,a) in enumerate(faqs))}
      </section>
      <section class="section">
        <div class="section-head"><h2>Related</h2></div>
        <div class="hub-grid">
          <a class="hub-link" href="../chart-vs-graph/">Chart vs graph <span>→</span></a>
          <a class="hub-link" href="../choose-a-chart-type/">Choose a chart type <span>→</span></a>
          <a class="hub-link" href="{prefix}chart-types/">Chart types <span>→</span></a>
        </div>
      </section>
{soft_cta(prefix)}
"""
    html = page_shell(
        title="Chart Glossary — Legend, Axis, Series & More | VIA",
        description=desc[:158],
        canonical=url,
        og_image=f"{BASE}/assets/og/home.png",
        prefix=prefix,
        nav_current="Learn",
        crumbs=[("Home", prefix), ("Learn", f"{prefix}learn/"), ("Glossary", None)],
        crumb_ld_items=[
            ("Home", f"{BASE}/"),
            ("Learn", f"{BASE}/learn/"),
            ("Glossary", url),
        ],
        schemas=[article_ld("Chart glossary", desc, url), defined, faq_ld(faqs)],
        body=body,
    )
    out = ROOT / "learn" / "glossary" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("wrote", out.relative_to(ROOT))


def write_mistakes() -> None:
    prefix = "../../"
    url = f"{BASE}/learn/common-chart-mistakes/"
    desc = "Common chart mistakes that hurt clarity: too many pie slices, truncated baselines, connecting unordered categories, radar overload, and treating spider as a separate type."
    mistakes = []
    for e in KG["entities"].values():
        if e.get("kind") != "chartType":
            continue
        for m in e.get("commonMistakes", []):
            mistakes.append((e["label"], m, e["slug"]))
    # dedupe keep order
    seen = set()
    cards = []
    for label, m, slug in mistakes:
        key = (label, m)
        if key in seen:
            continue
        seen.add(key)
        cards.append(
            f'<div class="callout"><strong>{esc(label)}:</strong> {esc(m)} '
            f'<a href="{prefix}{slug}/">Guide</a></div>'
        )
    faqs = [
        ("What’s the most common pie mistake?", "Too many slices. Cap at roughly 3–6 and group the rest as Other."),
        ("Is a truncated axis always wrong?", "It can exaggerate differences. If you truncate, say so — readers assume a zero baseline on bars."),
        ("Spider vs radar?", "Same idea educationally. VIA’s UI label is Radar, not Spider."),
    ]
    body = f"""
      <section class="hero">
        <p class="eyebrow">Clarity</p>
        <h1>Common chart mistakes.</h1>
        <p class="lead">These errors show up in homework, decks, and dashboards. Fix the question first, then the visual.</p>
      </section>
      <section class="section prose answer-block">
        <div class="section-head"><h2>Quick answer</h2></div>
        <p class="quick-answer">Most chart failures are mismatched intent: pie for ranking, line for unordered categories, radar for exact comparison, or bars with a truncated baseline that exaggerates gaps.</p>
      </section>
      <section class="section">
        <div class="section-head"><h2>Mistakes by chart type</h2></div>
        <div class="callouts">{''.join(cards)}</div>
      </section>
      <section class="section faq" id="questions">
        <div class="section-head"><h2>FAQ</h2></div>
        {''.join(f'<details{" open" if i==0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for i,(q,a) in enumerate(faqs))}
      </section>
      <section class="section">
        <div class="section-head"><h2>Related</h2></div>
        <div class="hub-grid">
          <a class="hub-link" href="../choose-a-chart-type/">Choose a chart type <span>→</span></a>
          <a class="hub-link" href="{prefix}compare/pie-vs-bar/">Pie vs bar <span>→</span></a>
          <a class="hub-link" href="{prefix}compare/">All comparisons <span>→</span></a>
        </div>
      </section>
{soft_cta(prefix)}
"""
    html = page_shell(
        title="Common Chart Mistakes to Avoid | VIA",
        description=desc[:158],
        canonical=url,
        og_image=f"{BASE}/assets/og/home.png",
        prefix=prefix,
        nav_current="Learn",
        crumbs=[
            ("Home", prefix),
            ("Learn", f"{prefix}learn/"),
            ("Common mistakes", None),
        ],
        crumb_ld_items=[
            ("Home", f"{BASE}/"),
            ("Learn", f"{BASE}/learn/"),
            ("Common chart mistakes", url),
        ],
        schemas=[article_ld("Common chart mistakes", desc, url), faq_ld(faqs)],
        body=body,
    )
    out = ROOT / "learn" / "common-chart-mistakes" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("wrote", out.relative_to(ROOT))


def write_chart_vs_graph() -> None:
    prefix = "../../"
    url = f"{BASE}/learn/chart-vs-graph/"
    desc = "Chart vs graph: in data visualization the words usually mean the same thing. In mathematics, a graph can mean nodes and edges — a different concept."
    faqs = [
        ("Are chart and graph the same?", "For everyday data viz, yes — people say pie chart or bar graph for the same class of visuals."),
        ("What about graph in math?", "A mathematical graph is vertices and edges. That is not a pie/bar/line chart."),
        ("Which term does VIA use?", "The App Store listing uses chart and graph; the app is a chart maker with ten chart types."),
    ]
    body = f"""
      <section class="hero">
        <p class="eyebrow">Terminology</p>
        <h1>Chart vs graph.</h1>
        <p class="lead">In school and business, the words usually point to the same thing: a visual of numbers. Context matters.</p>
      </section>
      <section class="section prose answer-block">
        <div class="section-head"><h2>Quick answer</h2></div>
        <p class="quick-answer">Use chart or graph interchangeably for pie, bar, and line visuals. Reserve “graph” for network/node diagrams when speaking with mathematicians or computer scientists.</p>
      </section>
      <section class="section">
        <div class="section-head"><h2>Side-by-side</h2></div>
        <div class="table-wrap">
          <table class="compare-table">
            <thead><tr><th>Context</th><th>Chart</th><th>Graph</th></tr></thead>
            <tbody>
              <tr><td>Homework / business</td><td>Common</td><td>Common (same idea)</td></tr>
              <tr><td>Data visualization literature</td><td>Preferred</td><td>Often synonym</td></tr>
              <tr><td>Mathematics / CS</td><td>Rare</td><td>Nodes + edges</td></tr>
            </tbody>
          </table>
        </div>
      </section>
      <section class="section faq" id="questions">
        <div class="section-head"><h2>FAQ</h2></div>
        {''.join(f'<details{" open" if i==0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for i,(q,a) in enumerate(faqs))}
      </section>
      <section class="section">
        <div class="section-head"><h2>Related</h2></div>
        <div class="hub-grid">
          <a class="hub-link" href="../glossary/">Glossary <span>→</span></a>
          <a class="hub-link" href="{prefix}graph-maker/">Graph maker hub <span>→</span></a>
          <a class="hub-link" href="../choose-a-chart-type/">Choose a chart type <span>→</span></a>
        </div>
      </section>
{soft_cta(prefix)}
"""
    html = page_shell(
        title="Chart vs Graph — What’s the Difference? | VIA",
        description=desc[:158],
        canonical=url,
        og_image=f"{BASE}/assets/og/graph-maker.png",
        prefix=prefix,
        nav_current="Learn",
        crumbs=[
            ("Home", prefix),
            ("Learn", f"{prefix}learn/"),
            ("Chart vs graph", None),
        ],
        crumb_ld_items=[
            ("Home", f"{BASE}/"),
            ("Learn", f"{BASE}/learn/"),
            ("Chart vs graph", url),
        ],
        schemas=[article_ld("Chart vs graph", desc, url), faq_ld(faqs)],
        body=body,
    )
    out = ROOT / "learn" / "chart-vs-graph" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("wrote", out.relative_to(ROOT))


def rewrite_compare_hub() -> None:
    prefix = "../"
    url = f"{BASE}/compare/"
    desc = "Compare chart types with decision rules: pie vs bar, bar vs line, line vs area, bar vs horizontal bar, pie vs donut, radar vs bar."
    links = "".join(
        f'<a class="dir-link" href="./{c["slug"]}/"><div><strong>{esc(c["title"])}</strong>'
        f'<span>{esc(c["decisionRule"][:72])}</span></div><span class="arrow">→</span></a>'
        for c in KG["comparisons"]
    )
    faqs = [
        ("Pie or bar?", entity("pie")["definition"][:80] + " Prefer bar for ranking."),
        ("Where is the chooser?", "See Choose a chart type under Learn."),
        ("Spider vs radar?", "Educational synonyms. VIA’s label is Radar."),
    ]
    body = f"""
      <section class="hero">
        <p class="eyebrow">Decide</p>
        <h1>Chart comparisons — full articles, not stubs.</h1>
        <p class="lead">Each pair has a quick answer, decision rule, comparison table, definitions, and mistakes. Product mentions only when VIA implements both sides.</p>
      </section>
      <section class="section">
        <div class="section-head"><h2>Comparisons</h2></div>
        <div class="dir-grid">{links}</div>
      </section>
      <section class="section faq" id="questions">
        <div class="section-head"><h2>FAQ</h2></div>
        {''.join(f'<details{" open" if i==0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for i,(q,a) in enumerate(faqs))}
      </section>
      <section class="section">
        <div class="section-head"><h2>Related</h2></div>
        <div class="hub-grid">
          <a class="hub-link" href="../learn/choose-a-chart-type/">Choose a chart type <span>→</span></a>
          <a class="hub-link" href="../chart-types/">Chart types <span>→</span></a>
          <a class="hub-link" href="../learn/">Learn hub <span>→</span></a>
        </div>
      </section>
{soft_cta(prefix)}
"""
    html = page_shell(
        title="Chart Comparisons — Pie vs Bar, Line vs Area | VIA",
        description=desc[:158],
        canonical=url,
        og_image=f"{BASE}/assets/og/graph-maker.png",
        prefix=prefix,
        nav_current="Compare",
        crumbs=[("Home", prefix), ("Compare", None)],
        crumb_ld_items=[("Home", f"{BASE}/"), ("Compare", url)],
        schemas=[article_ld("Chart comparisons", desc, url), faq_ld(faqs)],
        body=body,
    )
    (ROOT / "compare" / "index.html").write_text(html)
    print("rewrote compare/index.html")


def related_for_type(eid: str, prefix: str) -> str:
    e = entity(eid)
    links = []
    links.append((f"{prefix}chart-types/", "Chart types"))
    links.append((f"{prefix}learn/choose-a-chart-type/", "Choose a chart type"))
    for cid in e.get("comparesWith", []):
        for c in KG["comparisons"]:
            if {c["a"], c["b"]} == {eid, cid} or eid in (c["a"], c["b"]) and cid in (
                c["a"],
                c["b"],
            ):
                links.append((f"{prefix}compare/{c['slug']}/", c["title"]))
                break
        else:
            other = entity(cid)
            links.append((f"{prefix}{other['slug']}/", f"{other['label']} chart"))
    for rid in e.get("related", []):
        if rid in KG["entities"] and KG["entities"][rid].get("slug"):
            o = entity(rid)
            if o.get("kind") in ("chartType", "synonym"):
                links.append((f"{prefix}{o['slug']}/", f"{o['label']} chart"))
    links.append((f"{prefix}learn/common-chart-mistakes/", "Common mistakes"))
    links.append((f"{prefix}app/export/", "Export & Pro"))
    # dedupe
    seen = set()
    items = []
    for href, label in links:
        if href in seen:
            continue
        seen.add(href)
        items.append(f'<a class="hub-link" href="{href}">{esc(label)} <span>→</span></a>')
        if len(items) >= 8:
            break
    return (
        '        <div class="hub-grid">\n          '
        + "\n          ".join(items)
        + "\n        </div>"
    )


def patch_nav_all() -> None:
    nav_re = re.compile(r"<nav class=\"nav-links\"[^>]*>.*?</nav>", re.S)
    for path in ROOT.rglob("index.html"):
        rel = path.relative_to(ROOT)
        depth = len(rel.parts) - 1
        prefix = "../" * depth if depth else ""
        # determine current
        current = None
        parts = rel.parts
        if parts[0] == "compare":
            current = "Compare"
        elif parts[0] == "learn":
            current = "Learn"
        elif parts[0] == "tools":
            current = "Tools"
        elif parts[0] == "chart-types":
            current = "Types"
        html = path.read_text()
        if "nav-links" not in html:
            continue
        new_nav = nav_html(prefix if prefix else "./" if depth == 0 else prefix, current)
        # homepage prefix for links should be empty string style: pie-chart/ not ./pie
        if depth == 0:
            new_nav = nav_html("", current).replace('href="chart-types/"', 'href="chart-types/"')
            # nav_html with "" gives href="chart-types/" which is correct
            new_nav = (
                '<nav class="nav-links" aria-label="Sections">\n'
                '        <a href="chart-types/">Types</a>\n'
                '        <a href="compare/">Compare</a>\n'
                '        <a href="learn/">Learn</a>\n'
                '        <a href="tools/">Tools</a>\n'
                "      </nav>"
            )
        html2 = nav_re.sub(new_nav, html, count=1)
        if html2 != html:
            path.write_text(html2)
    print("patched nav sitewide")


def patch_type_related_and_geo() -> None:
    """Inject GEO blocks and related links into chart type pages from KG."""
    for eid, e in KG["entities"].items():
        if e.get("kind") not in ("chartType", "synonym") or not e.get("slug"):
            continue
        path = ROOT / e["slug"] / "index.html"
        if not path.exists():
            continue
        html = path.read_text()
        prefix = "../"
        # Fix related section
        related_html = related_for_type(
            e["mapsTo"] if e.get("kind") == "synonym" else eid, prefix
        )
        html = re.sub(
            r'(<div class="section-head">\s*<h2>Related pages</h2>\s*</div>\s*)<div class="hub-grid">.*?</div>',
            r"\1" + related_html,
            html,
            count=1,
            flags=re.S,
        )
        # Also match "Related"
        html = re.sub(
            r'(<div class="section-head"><h2>Related</h2></div>\s*)<div class="hub-grid">.*?</div>',
            r"\1" + related_html,
            html,
            count=1,
            flags=re.S,
        )

        # Inject definition + mistakes before FAQ if missing
        if 'class="quick-answer"' not in html and e.get("definition"):
            inject = f"""
      <section class="section prose answer-block">
        <div class="section-head"><h2>Definition</h2></div>
        <p class="quick-answer">{esc(e['definition'])}</p>
      </section>
"""
            if e.get("commonMistakes"):
                inject += f"""
      <section class="section">
        <div class="section-head"><h2>Common mistakes</h2></div>
        <div class="callouts">
          {''.join(f'<div class="callout">{esc(m)}</div>' for m in e['commonMistakes'])}
        </div>
      </section>
"""
            html = html.replace(
                '<section class="section faq" id="questions">',
                inject + '\n      <section class="section faq" id="questions">',
                1,
            )

        # Fix under-listed type phrases
        html = html.replace(
            "Pie, bar, line, and radar, plus styling and export options beyond the browser tools.",
            f"VIA includes {TYPES_LABEL}.",
        )
        html = html.replace(
            "VIA is a native iOS app for line, pie, bar, and radar charts — no spreadsheet required.",
            f"Yes. VIA is a native iOS app with {TYPES_LABEL} — no spreadsheet required.",
        )
        html = re.sub(
            r"line, pie, bar, and radar",
            TYPES_LABEL,
            html,
        )
        html = re.sub(
            r"pie, bar, line, and radar",
            TYPES_LABEL,
            html,
        )

        # Ensure breadcrumb UI exists
        if 'class="breadcrumbs"' not in html:
            label = e.get("label", e["slug"])
            crumb = crumbs_html(
                [
                    ("Home", prefix),
                    ("Chart types", f"{prefix}chart-types/"),
                    (label, None),
                ]
            )
            html = html.replace("<main>", crumb + "\n    <main>", 1)

        path.write_text(html)
        print("patched type", e["slug"])


def patch_accuracy_faqs() -> None:
    replacements = {
        "chart-app/index.html": [
            (
                "Pie, bar, line, and radar, plus styling and export options beyond the browser tools.",
                f"VIA includes {TYPES_LABEL}.",
            ),
            (
                "<p>Pie, bar, line, and radar, plus styling and export options beyond the browser tools.</p>",
                f"<p>VIA includes {TYPES_LABEL}.</p>",
            ),
        ],
        "line-chart/index.html": [
            (
                "Yes. VIA is a native iOS app for line, pie, bar, and radar charts — no spreadsheet required.",
                f"Yes. VIA is a native iOS app with {TYPES_LABEL} — no spreadsheet required.",
            ),
        ],
        "on-phone/index.html": [
            (
                "a native chart app for pie, bar, line, and radar",
                "a native chart app with ten chart types",
            ),
        ],
        "homework/index.html": [
            (
                "or use VIA for line and radar charts",
                "or use VIA for ten chart types",
            ),
        ],
    }
    for rel, pairs in replacements.items():
        path = ROOT / rel
        if not path.exists():
            continue
        html = path.read_text()
        for a, b in pairs:
            html = html.replace(a, b)
        # visible FAQ bodies
        html = html.replace(
            "Pie, bar, line, and radar charts in a phone-native editor.",
            f"Ten types: {TYPES_LABEL}.",
        )
        path.write_text(html)
    print("patched accuracy FAQs")


def patch_home_directory() -> None:
    path = ROOT / "index.html"
    html = path.read_text()
    # nav already patched
    block = """
      <section class="section">
        <div class="section-head"><h2>Learn & compare</h2></div>
        <div class="dir-grid">
          <a class="dir-link" href="learn/choose-a-chart-type/"><div><strong>Choose a chart type</strong><span>Decision rules</span></div><span class="arrow">→</span></a>
          <a class="dir-link" href="compare/pie-vs-bar/"><div><strong>Pie vs bar</strong><span>Shares vs ranking</span></div><span class="arrow">→</span></a>
          <a class="dir-link" href="compare/bar-vs-line/"><div><strong>Bar vs line</strong><span>Categories vs trends</span></div><span class="arrow">→</span></a>
          <a class="dir-link" href="learn/glossary/"><div><strong>Glossary</strong><span>Legend, axis, series</span></div><span class="arrow">→</span></a>
          <a class="dir-link" href="learn/common-chart-mistakes/"><div><strong>Common mistakes</strong><span>Clarity failures</span></div><span class="arrow">→</span></a>
          <a class="dir-link" href="learn/"><div><strong>Learn hub</strong><span>All guides</span></div><span class="arrow">→</span></a>
        </div>
      </section>"""
    if "learn/choose-a-chart-type/" not in html:
        # insert before FAQ
        html = html.replace(
            '<section class="section faq" id="questions">',
            block + '\n      <section class="section faq" id="questions">',
            1,
        )
    if 'class="breadcrumbs"' not in html:
        html = html.replace(
            "<main>",
            crumbs_html([("Home", None)]) + "\n    <main>",
            1,
        )
    path.write_text(html)
    print("patched home directory")


def patch_app_software_schema() -> None:
    sa = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "VIA",
        "operatingSystem": "iOS 18.6+",
        "applicationCategory": "UtilitiesApplication",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "url": APP,
        "description": f"Native iOS chart maker for {TYPES_LABEL}. Export PNG, JPEG, PDF. Local projects; no Excel import.",
    }
    for rel in ["app/index.html", "chart-app/index.html", "app/export/index.html"]:
        path = ROOT / rel
        if not path.exists():
            continue
        html = path.read_text()
        if '"@type": "SoftwareApplication"' in html or '"@type":"SoftwareApplication"' in html:
            continue
        snippet = f'  <script type="application/ld+json">\n{jd(sa)}\n  </script>\n'
        html = html.replace("</head>", snippet + "</head>", 1)
        path.write_text(html)
    print("added SoftwareApplication schema")


def write_feed_and_sitemap_llms() -> None:
    urls = [
        f"{BASE}/",
        f"{BASE}/tools/",
        f"{BASE}/chart-types/",
        f"{BASE}/how-to/",
        f"{BASE}/compare/",
        f"{BASE}/learn/",
        f"{BASE}/learn/choose-a-chart-type/",
        f"{BASE}/learn/glossary/",
        f"{BASE}/learn/common-chart-mistakes/",
        f"{BASE}/learn/chart-vs-graph/",
        f"{BASE}/app/",
        f"{BASE}/app/supported-chart-types/",
        f"{BASE}/app/export/",
    ]
    for e in KG["entities"].values():
        if e.get("slug") and e.get("kind") in ("chartType", "synonym"):
            urls.append(f"{BASE}/{e['slug']}/")
    for c in KG["comparisons"]:
        urls.append(f"{BASE}/compare/{c['slug']}/")
    for p in [
        "from-table",
        "on-phone",
        "homework",
        "chart-app",
        "graph-maker",
    ]:
        urls.append(f"{BASE}/{p}/")
    # unique preserve order
    seen = set()
    ordered = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            ordered.append(u)

    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in ordered:
        sm.append(
            f"  <url><loc>{u}</loc><lastmod>{KG['verifiedAt']}</lastmod></url>"
        )
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n")

    items = []
    for c in KG["comparisons"]:
        items.append(
            f"""    <item>
      <title>{esc(c['title'])}</title>
      <link>{BASE}/compare/{c['slug']}/</link>
      <guid>{BASE}/compare/{c['slug']}/</guid>
      <description>{esc(c['quickAnswer'])}</description>
      <pubDate>Sun, 03 Aug 2026 12:00:00 GMT</pubDate>
    </item>"""
        )
    for path, title, desc in [
        ("learn/choose-a-chart-type/", "Choose a chart type", "Decision rules for picking a chart"),
        ("learn/glossary/", "Chart glossary", "Definitions for chart vocabulary"),
        ("learn/common-chart-mistakes/", "Common chart mistakes", "Clarity failures to avoid"),
        ("learn/chart-vs-graph/", "Chart vs graph", "Terminology guide"),
    ]:
        items.append(
            f"""    <item>
      <title>{esc(title)}</title>
      <link>{BASE}/{path}</link>
      <guid>{BASE}/{path}</guid>
      <description>{esc(desc)}</description>
      <pubDate>Sun, 03 Aug 2026 12:00:00 GMT</pubDate>
    </item>"""
        )
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>VIA Chart Guides</title>
    <link>{BASE}/</link>
    <description>Educational chart and data visualization guides from VIA.</description>
    <language>en-us</language>
{chr(10).join(items)}
  </channel>
</rss>
"""
    (ROOT / "feed.xml").write_text(feed)

    llms = f"""# VIA Chart Maker

> Educational data-visualization site plus free browser pie/bar tools. Native iOS app: VIA. Source of truth: `knowledge-graph.json` + `product-knowledge.json` (synced from ChartBuilder).

## Entity
- Name: VIA (VIA Chart Builder / Graph Maker)
- Bundle ID: {KG['product']['bundleId']}
- Platform: native iOS / iPadOS ({KG['product']['minimumOS']}+)
- Developer: {KG['product']['developer']}
- App Store: {APP}
- Website: {BASE}/
- RSS: {BASE}/feed.xml

## Chart types in VIA (UI labels)
Pie, Donut, Line, Area, Bar, H. Bar, Stacked, Scatter, Radar, Gantt.

## Browser tools
- Pie and bar makers only
- No Excel/CSV import
- No automatic browser → app handoff

## Export
- PNG, JPEG, PDF · sizes to 3840×2160 · White / Transparent / Dark
- Pro required to export: Stacked, Scatter, Radar, Gantt
- Free caps: 1 saved project, 3 custom colors

## Hubs
- [Chart types]({BASE}/chart-types/)
- [Compare]({BASE}/compare/)
- [Learn]({BASE}/learn/)
- [Tools]({BASE}/tools/)
- [How-to]({BASE}/how-to/)
- [App]({BASE}/app/) · [Export]({BASE}/app/export/)

## Learn
- [Choose a chart type]({BASE}/learn/choose-a-chart-type/)
- [Glossary]({BASE}/learn/glossary/)
- [Common mistakes]({BASE}/learn/common-chart-mistakes/)
- [Chart vs graph]({BASE}/learn/chart-vs-graph/)

## Comparisons
{chr(10).join(f"- [{c['title']}]({BASE}/compare/{c['slug']}/)" for c in KG['comparisons'])}

## Citation rules
- Prefer the page matching the chart type, comparison, or intent.
- Do not claim Excel import, multi-series, dashboards, or web→app continuation.
- Spider chart → VIA label is Radar.
- Product limits: see knowledge-graph.json capabilities.notSupported.
"""
    (ROOT / "llms.txt").write_text(llms)
    print(f"sitemap ({len(ordered)} urls), feed.xml, llms.txt updated")


def add_css() -> None:
    css_path = ROOT / "styles.css"
    css = css_path.read_text()
    if ".breadcrumbs" in css:
        return
    css += """

/* Breadcrumbs */
.breadcrumbs {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px 8px;
  margin: -12px 0 28px;
  font-size: 0.82rem;
  color: var(--muted);
}
.breadcrumbs a {
  color: var(--accent-2);
  text-decoration: none;
}
.breadcrumbs a:hover {
  text-decoration: underline;
}
.crumb-sep {
  color: var(--soft);
}

/* GEO answer blocks */
.answer-block .quick-answer {
  font-size: 1.05rem;
  line-height: 1.55;
  color: var(--ink-2);
  margin: 0 0 12px;
}
.lead-sm {
  color: var(--muted);
  max-width: 40rem;
}

/* Comparison tables */
.table-wrap {
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: var(--card);
}
.compare-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.92rem;
}
.compare-table th,
.compare-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}
.compare-table th {
  background: #f1f5f9;
  font-weight: 650;
}
.compare-table tr:last-child td {
  border-bottom: 0;
}

.glossary-list {
  display: grid;
  gap: 16px;
}
.glossary-item {
  padding: 14px 0;
  border-bottom: 1px solid var(--line);
}
.glossary-item:last-child {
  border-bottom: 0;
}
.glossary-item h3 {
  margin: 0 0 6px;
  font-family: var(--display);
  font-size: 1.15rem;
}
.glossary-item p {
  margin: 0;
  color: var(--ink-2);
}

.cta-band {
  border-top: 1px solid var(--line);
  padding-top: 8px;
}
"""
    css_path.write_text(css)
    print("styles.css extended")


def main() -> None:
    for c in KG["comparisons"]:
        comparison_page(c)
    write_learn_hub()
    write_chooser()
    write_glossary()
    write_mistakes()
    write_chart_vs_graph()
    rewrite_compare_hub()
    add_css()
    patch_nav_all()
    patch_type_related_and_geo()
    patch_accuracy_faqs()
    patch_home_directory()
    patch_app_software_schema()
    write_feed_and_sitemap_llms()
    print("done")


if __name__ == "__main__":
    main()
