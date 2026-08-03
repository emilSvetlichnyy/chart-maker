#!/usr/bin/env python3
"""Apply Full Audit fixes: keyword coverage, metas/titles, GEO bylines, thin content."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KG = json.loads((ROOT / "knowledge-graph.json").read_text())
BASE = KG["product"]["siteBase"]
APP = KG["product"]["appStoreUrl"]
DEV = KG["product"]["developerUrl"]
AUTHOR = KG["product"]["developer"]
DATE = "2026-08-03"

TYPE_COPY = {
    "pie": {
        "title": "Free Pie Chart Maker Online — VIA",
        "meta": "Free pie chart maker online: enter labels and values, preview instantly, download a PNG. Learn pie chart data visualization, then use VIA on iPhone.",
        "primary": "pie chart maker",
        "extra": """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>What is a pie chart maker?</h2></div>
        <p>A <strong>pie chart maker</strong> turns category labels and numbers into a circular chart so readers see each slice as a share of one total. Students and marketers use a free pie chart maker for budgets, survey results, and market shares — classic <strong>data visualization</strong> for part-to-whole questions.</p>
        <p>This page is an <strong>online pie chart maker</strong> with a live preview and PNG download. For a native <strong>chart maker app</strong> on iPhone — including donut, line, bar, and more chart types — open VIA and re-enter your values (there is no automatic handoff).</p>
        <h3>How to make a pie chart fast</h3>
        <ol>
          <li>Type each category name and numeric value.</li>
          <li>Keep 3–6 slices; group leftovers as “Other”.</li>
          <li>Download a PNG, or rebuild the same chart in the VIA graph maker on iPhone.</li>
        </ol>
      </section>""",
    },
    "bar": {
        "title": "Free Bar Chart Maker Online — VIA",
        "meta": "Free bar chart maker online: compare categories, preview live, download a PNG. Learn bar chart data visualization for ranking, then use VIA on iPhone.",
        "primary": "bar chart maker",
        "extra": """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>What is a bar chart maker?</h2></div>
        <p>A <strong>bar chart maker</strong> encodes values as bar lengths so you can compare categories at a glance. It is one of the most common <strong>data visualization</strong> tools for rankings, survey scores, and sales by product.</p>
        <p>Use this <strong>free bar chart maker</strong> in the browser, or continue in VIA — a <strong>chart maker app</strong> / <strong>graph maker</strong> for iPhone with ten chart types including horizontal bar, stacked bar, line, and scatter.</p>
        <h3>When to use a bar chart vs a pie chart</h3>
        <p>Choose a <strong>bar chart</strong> to compare magnitudes. Choose a <strong>pie chart</strong> only when categories are shares of one total and you have few slices. See <a href="../compare/pie-vs-bar/">pie chart vs bar chart</a>.</p>
      </section>""",
    },
    "donut": {
        "title": "Donut Chart Maker for iPhone — VIA",
        "meta": "Learn donut chart data visualization and make a donut chart on iPhone with VIA. Same part-to-whole job as a pie chart, with space for a center total.",
        "extra": """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>What is a donut chart?</h2></div>
        <p>A <strong>donut chart</strong> is a pie chart with an open center — useful when you want a total or KPI in the middle. It is still part-to-whole <strong>data visualization</strong>, not a different analysis than a pie chart.</p>
        <p>This site’s browser tool is a <strong>pie chart maker</strong> (with a visual hole). True <strong>Donut</strong> charts are built in the VIA <strong>chart maker app</strong> on iPhone. Compare options in <a href="../compare/pie-vs-donut/">pie vs donut</a>.</p>
      </section>""",
    },
    "line": {
        "title": "Line Chart Maker for iPhone — VIA",
        "meta": "Make a line chart on iPhone with VIA, a native chart maker app. Track trends over time with clear data visualization — free to start, export PNG when ready.",
        "extra": """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>What is a line chart maker?</h2></div>
        <p>A <strong>line chart maker</strong> connects ordered values to show change — usually over time. It is the default <strong>data visualization</strong> choice for trends, growth, and rate of change.</p>
        <p>There is no live browser line tool here (online makers cover pie and bar). Use VIA as your <strong>line chart maker</strong> / <strong>graph maker</strong> on iPhone. Compare with bars in <a href="../compare/bar-vs-line/">bar chart vs line chart</a>.</p>
      </section>""",
    },
    "area": {
        "title": "Area Chart Maker for iPhone — VIA",
        "meta": "Make an area chart on iPhone with VIA. Area charts fill under a line for volume-focused data visualization — export PNG, JPEG, or PDF from the chart maker app.",
        "extra": """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>What is an area chart?</h2></div>
        <p>An <strong>area chart</strong> is a line chart with the region under the line filled. Use it when magnitude/volume matters as much as direction in your <strong>data visualization</strong>.</p>
        <p>Build area charts in the VIA <strong>chart maker app</strong> on iPhone. See <a href="../compare/line-vs-area/">line chart vs area chart</a> for the decision rule.</p>
      </section>""",
    },
    "horizontalBar": {
        "title": "Horizontal Bar Chart Maker — VIA",
        "meta": "Make a horizontal bar chart (H. Bar) on iPhone with VIA. Best bar chart layout for long labels and ranked lists — native chart maker app, export PNG.",
        "extra": """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>What is a horizontal bar chart?</h2></div>
        <p>A <strong>horizontal bar chart</strong> (VIA label: <strong>H. Bar</strong>) draws bars sideways so long category names stay readable. It is a core <strong>bar chart</strong> variant in <strong>data visualization</strong> for rankings and surveys.</p>
        <p>Compare layouts in <a href="../compare/bar-vs-horizontal-bar/">bar chart vs horizontal bar chart</a>. Create H. Bar charts in the VIA <strong>graph maker</strong> on iPhone.</p>
      </section>""",
    },
    "stackedBar": {
        "title": "Stacked Bar Chart Maker for iPhone — VIA",
        "meta": "Make a stacked bar chart on iPhone with VIA. Show composition inside a total with clear data visualization. Export requires VIA Pro for Stacked charts.",
        "extra": """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>What is a stacked bar chart?</h2></div>
        <p>A <strong>stacked bar chart</strong> shows how segments add up to a total inside a bar — useful composition <strong>data visualization</strong> when a simple pie chart is not enough.</p>
        <p>In VIA the UI label is <strong>Stacked</strong>. Exporting Stacked charts requires Pro. Learn the type on this page, then build it in the <strong>chart maker app</strong>.</p>
      </section>""",
    },
    "scatter": {
        "title": "Scatter Plot Chart Maker for iPhone — VIA",
        "meta": "Make a scatter chart (scatter plot) on iPhone with VIA. Plot X and Y for correlation-style data visualization. Exporting Scatter requires VIA Pro.",
        "extra": """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>What is a scatter chart?</h2></div>
        <p>A <strong>scatter chart</strong> (scatter plot) places each point by X and Y values to reveal relationships, clusters, and outliers — essential scientific <strong>data visualization</strong>.</p>
        <p>Build scatter plots in the VIA <strong>chart maker app</strong>. Exporting Scatter requires Pro. Free users can still select and edit the type.</p>
      </section>""",
    },
    "radar": {
        "title": "Radar Chart Maker (Spider Chart) — VIA",
        "meta": "Make a radar chart (spider chart) on iPhone with VIA. Compare multi-attribute profiles with native data visualization. Exporting Radar requires VIA Pro.",
        "extra": """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>What is a radar chart maker?</h2></div>
        <p>A <strong>radar chart maker</strong> plots scores on axes around a center — also called a <strong>spider chart</strong> or web chart in education. VIA’s UI label is <strong>Radar</strong>.</p>
        <p>Use radar for skill/product profiles; use a <strong>bar chart</strong> when exact ranking matters. See <a href="../compare/radar-vs-bar/">radar chart vs bar chart</a>. Exporting Radar requires Pro.</p>
      </section>""",
    },
    "gantt": {
        "title": "Gantt Chart Maker for iPhone — VIA",
        "meta": "Make a gantt chart on iPhone with VIA. Plan task timelines with start and end dates — project-style data visualization. Exporting Gantt requires VIA Pro.",
        "extra": """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>What is a gantt chart maker?</h2></div>
        <p>A <strong>gantt chart maker</strong> shows tasks as bars across dates so duration and overlap are visible — timeline <strong>data visualization</strong> for school projects and simple schedules.</p>
        <p>VIA includes Gantt as a native chart type in the <strong>chart maker app</strong>. Exporting Gantt requires Pro.</p>
      </section>""",
    },
}


def set_title_meta(html: str, title: str, meta: str) -> str:
    if len(title) < 30:
        title = (title + " | Chart Maker").strip()[:60]
    if len(title) > 60:
        title = title[:57].rstrip() + "…"
    if len(meta) < 140:
        meta = (meta + " Learn clear data visualization with VIA.").strip()[:160]
    if len(meta) > 160:
        meta = meta[:157].rstrip() + "…"
    assert 30 <= len(title) <= 60, (len(title), title)
    assert 140 <= len(meta) <= 160, (len(meta), meta)
    html = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", html, count=1)
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{meta}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{title}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{meta}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{title}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="{meta}">',
        html,
        count=1,
    )
    return html


AUTHOR_NOTE = f"""      <p class="author-note">Guide by <a href="{DEV}">{AUTHOR}</a>, indie iOS developer of VIA. Updated {DATE}. Product claims verified against the ChartBuilder iOS codebase.</p>"""


def ensure_author(html: str) -> str:
    if 'class="author-note"' in html:
        return html
    # before footer
    return html.replace(
        '<footer class="site-footer">',
        AUTHOR_NOTE + '\n    <footer class="site-footer">',
        1,
    )


def ensure_crumb(html: str, crumbs_html: str) -> str:
    if 'class="breadcrumbs"' in html:
        return html
    return html.replace("<main>", crumbs_html + "\n    <main>", 1)


def inject_before_faq(html: str, block: str) -> str:
    if "keyword-block" in html:
        return html
    if '<section class="section faq"' in html:
        return html.replace(
            '<section class="section faq"',
            block + '\n      <section class="section faq"',
            1,
        )
    return html


def enrich_types() -> None:
    id_by_slug = {
        e["slug"]: eid
        for eid, e in KG["entities"].items()
        if e.get("kind") == "chartType" and e.get("slug")
    }
    for slug, eid in id_by_slug.items():
        conf = TYPE_COPY.get(eid)
        if not conf:
            continue
        path = ROOT / slug / "index.html"
        html = path.read_text()
        if "title" in conf and "meta" in conf:
            html = set_title_meta(html, conf["title"], conf["meta"])
        html = inject_before_faq(html, conf["extra"])
        html = ensure_author(html)
        html = ensure_crumb(
            html,
            f'<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../">Home</a><span class="crumb-sep" aria-hidden="true">›</span><a href="../chart-types/">Chart types</a><span class="crumb-sep" aria-hidden="true">›</span><span aria-current="page">{KG["entities"][eid]["label"]}</span></nav>',
        )
        path.write_text(html)
        print("enriched", slug)


def enrich_home() -> None:
    path = ROOT / "index.html"
    html = path.read_text()
    html = set_title_meta(
        html,
        "Free Chart Maker Online & iPhone — VIA",
        "Free chart maker and graph maker online for pie and bar charts, plus VIA — a native iPhone chart maker app with ten chart types for data visualization.",
    )
    html = html.replace(
        "<h1>VIA — free browser charts, ten types on iPhone.</h1>",
        "<h1>Free chart maker online — and on iPhone.</h1>",
    )
    html = html.replace(
        """        <p class="lead">
          Enter numbers here for a free pie or bar chart and download a PNG —
          no signup. For other chart types or saved projects, use VIA on iPhone
          and enter values in the app.
        </p>""",
        """        <p class="lead">
          Use this free chart maker / graph maker to build a pie chart or bar chart
          online and download a PNG — no signup. For full data visualization with
          ten chart types on iPhone, open the VIA chart maker app and re-enter values.
        </p>""",
    )
    html = html.replace(
        "<h3>Pie, bar, or line</h3>\n            <p>Use pie for shares, bar to compare values, line for trends over time (line is in the app).</p>",
        "<h3>Chart types that match the question</h3>\n            <p>Pie chart for shares, bar chart to compare, line chart for trends, plus area, scatter, radar, gantt, and more in the VIA chart maker app.</p>",
    )
    block = """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>What is a chart maker?</h2></div>
        <p class="quick-answer">A <strong>chart maker</strong> (also called a <strong>graph maker</strong>) turns numbers into visuals — pie charts, bar charts, line charts, and other chart types — so people understand data faster than from a spreadsheet alone.</p>
        <p>This website offers a free online chart maker for pie and bar charts, plus educational guides on <strong>data visualization</strong>, choosing chart types, and common chart mistakes. VIA is the native iOS chart maker app when you need saved projects and more chart types on iPhone.</p>
        <h3>Popular ways people use this site</h3>
        <ul>
          <li><a href="pie-chart/">Pie chart maker</a> — parts of a whole, homework, budgets</li>
          <li><a href="bar-chart/">Bar chart maker</a> — compare categories and rankings</li>
          <li><a href="learn/choose-a-chart-type/">Choose a chart type</a> — decision rules before you draw</li>
          <li><a href="compare/pie-vs-bar/">Pie chart vs bar chart</a> — pick the clearer visual</li>
          <li><a href="graph-maker/">Graph maker hub</a> — chart vs graph wording</li>
        </ul>
      </section>"""
    html = inject_before_faq(html, block)
    path.write_text(html)
    print("enriched home")


def enrich_hubs() -> None:
    hubs = {
        "tools/index.html": (
            "Free Online Chart Maker Tools — Pie & Bar",
            "Free online chart maker tools for pie charts and bar charts. Preview live, download PNG, no signup. Learn data visualization limits: no Excel import, no app handoff.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>Online chart maker tools</h2></div>
        <p class="quick-answer">These browser tools are a free <strong>chart maker</strong> and <strong>graph maker</strong> for two chart types: pie chart and bar chart. Enter labels and values, preview, download a PNG.</p>
        <p>For line charts, radar charts, scatter plots, gantt charts, and other <strong>chart types</strong>, use the VIA <strong>chart maker app</strong> on iPhone. Start with <a href="../learn/choose-a-chart-type/">how to choose a chart type</a>.</p>
      </section>""",
            '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../">Home</a><span class="crumb-sep" aria-hidden="true">›</span><span aria-current="page">Tools</span></nav>',
        ),
        "chart-types/index.html": (
            "Chart Types Guide — Pie, Bar, Line & More",
            "Explore chart types for clearer data visualization: pie, donut, line, area, bar, horizontal bar, stacked, scatter, radar, and gantt — with VIA app notes.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>Which chart types should you learn first?</h2></div>
        <p class="quick-answer">Start with <strong>pie chart</strong> (parts of a whole), <strong>bar chart</strong> (compare categories), and <strong>line chart</strong> (trends). Then add area, scatter, radar, and gantt as your <strong>data visualization</strong> questions get more specific.</p>
        <p>VIA’s <strong>chart maker app</strong> includes ten chart types. Browser <strong>chart maker</strong> tools on this site cover pie and bar only. Use the <a href="../learn/choose-a-chart-type/">chart type decision guide</a> before you open any tool.</p>
      </section>""",
            None,
        ),
        "learn/index.html": (
            "Learn Data Visualization & Chart Design",
            "Learn data visualization and chart design: choose a chart type, chart glossary, common chart mistakes, and chart vs graph — educational guides from VIA.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>Why learn chart design before the tool?</h2></div>
        <p class="quick-answer"><strong>Data visualization</strong> fails when the chart type does not match the question. These guides teach chart types, graph maker vocabulary, and mistakes — so any chart maker (including VIA) produces clearer results.</p>
      </section>""",
            None,
        ),
        "graph-maker/index.html": (
            "Free Graph Maker Online & iPhone — VIA",
            "Free graph maker for pie and bar charts online, plus VIA on iPhone for ten chart types. Chart maker / graph maker wording explained — download a PNG free.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>Graph maker or chart maker?</h2></div>
        <p class="quick-answer">People search both <strong>graph maker</strong> and <strong>chart maker</strong> for the same job: turn numbers into a pie chart, bar chart, or line chart. On this site, the free online graph maker covers pie and bar; VIA is the iPhone chart maker app for more chart types.</p>
        <p>See <a href="../learn/chart-vs-graph/">chart vs graph</a> and the <a href="../pie-chart/">pie chart maker</a> / <a href="../bar-chart/">bar chart maker</a> tools.</p>
      </section>""",
            '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../">Home</a><span class="crumb-sep" aria-hidden="true">›</span><span aria-current="page">Graph maker</span></nav>',
        ),
        "chart-app/index.html": (
            "Chart Maker App for iPhone — VIA",
            "VIA is a native iPhone chart maker app and graph maker with ten chart types for data visualization. Export PNG, JPEG, PDF — free to start, no Excel required.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>What makes a good chart maker app?</h2></div>
        <p class="quick-answer">A strong <strong>chart maker app</strong> lets you pick a chart type, enter values quickly, preview, and export — without forcing a full spreadsheet. VIA focuses on phone-first <strong>data visualization</strong> for pie, bar, line, area, scatter, radar, gantt, and more.</p>
      </section>""",
            '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../">Home</a><span class="crumb-sep" aria-hidden="true">›</span><a href="../app/">App</a><span class="crumb-sep" aria-hidden="true">›</span><span aria-current="page">Chart app</span></nav>',
        ),
        "on-phone/index.html": (
            "How to Make a Chart on iPhone — VIA",
            "Make a graph or chart on iPhone without Excel: free online pie chart maker and bar chart maker in Safari, or install VIA — a native chart maker app.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>How do you make a chart on iPhone?</h2></div>
        <p class="quick-answer">Use a browser <strong>chart maker</strong> for a quick pie chart or bar chart PNG, or install a native <strong>chart maker app</strong> like VIA for more chart types, saved projects, and export options.</p>
        <p>This guide covers both paths for phone-first <strong>data visualization</strong> — no spreadsheet required.</p>
      </section>""",
            '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../">Home</a><span class="crumb-sep" aria-hidden="true">›</span><a href="../how-to/">How-to</a><span class="crumb-sep" aria-hidden="true">›</span><span aria-current="page">On iPhone</span></nav>',
        ),
        "homework/index.html": (
            "Charts for Homework — Free Chart Maker",
            "Make charts for homework on iPhone: free online pie chart maker or bar chart maker for a PNG, or use VIA for more chart types. Student-friendly data visualization.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>Best chart types for homework</h2></div>
        <p class="quick-answer">Most school assignments need a <strong>pie chart</strong> (shares), <strong>bar chart</strong> (compare), or <strong>line chart</strong> (change over time). Start with a free online chart maker, then expand in the VIA graph maker if you need other chart types.</p>
      </section>""",
            '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../">Home</a><span class="crumb-sep" aria-hidden="true">›</span><a href="../how-to/">How-to</a><span class="crumb-sep" aria-hidden="true">›</span><span aria-current="page">Homework</span></nav>',
        ),
        "from-table/index.html": (
            "Make a Chart from Excel or Sheets — VIA",
            "Turn Excel or Google Sheets numbers into a chart by typing values into a free pie chart maker or bar chart maker. No Excel import — clear data visualization steps.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>How to make a chart from a table</h2></div>
        <p class="quick-answer">Keep two columns visible (name + number), then type them into an online <strong>chart maker</strong> or into VIA. There is no Excel/CSV import — this workflow is honest manual entry for clean <strong>data visualization</strong>.</p>
      </section>""",
            '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../">Home</a><span class="crumb-sep" aria-hidden="true">›</span><a href="../how-to/">How-to</a><span class="crumb-sep" aria-hidden="true">›</span><span aria-current="page">From table</span></nav>',
        ),
        "how-to/index.html": (
            "How to Make a Chart — Practical Guides",
            "How to make a chart on iPhone, for homework, or from a table. Practical chart maker guides with honest limits — no fake Excel import. Start free online.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>How to make a chart (start here)</h2></div>
        <p class="quick-answer">Pick the chart type for your question, enter values in a <strong>chart maker</strong> or <strong>graph maker</strong>, then export a PNG. Use <a href="../learn/choose-a-chart-type/">choose a chart type</a> if you are unsure whether you need a pie chart, bar chart, or line chart.</p>
      </section>""",
            None,
        ),
        "compare/index.html": (
            "Chart Comparisons — Pie vs Bar & More",
            "Compare chart types for better data visualization: pie chart vs bar chart, bar vs line, line vs area, and more — decision rules before you open a chart maker.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>Why compare chart types?</h2></div>
        <p class="quick-answer">The same numbers can mislead in the wrong visual. These comparisons help you choose between a pie chart, bar chart, line chart, and other chart types before you use any chart maker.</p>
      </section>""",
            None,
        ),
        "app/index.html": (
            "VIA Chart Maker App for iPhone",
            "VIA is a native iPhone chart maker and graph maker with ten chart types, local projects, and PNG/JPEG/PDF export. Honest limits: no Excel import, no cloud sync.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>VIA chart maker app — verified capabilities</h2></div>
        <p class="quick-answer">VIA is a native <strong>chart maker app</strong> for iPhone and iPad with pie, donut, line, area, bar, H. Bar, stacked, scatter, radar, and gantt. Export PNG, JPEG, or PDF. Free tier: one saved project and three custom colors.</p>
      </section>""",
            '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../">Home</a><span class="crumb-sep" aria-hidden="true">›</span><span aria-current="page">App</span></nav>',
        ),
        "app/export/index.html": (
            "Export Charts — PNG, JPEG, PDF | VIA",
            "Export charts from the VIA chart maker app as PNG, JPEG, or PDF. Sizes, backgrounds, Save to Photos, and which chart types require Pro to export.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>How do you export a chart from VIA?</h2></div>
        <p class="quick-answer">Open Export in the <strong>chart maker app</strong>, pick PNG, JPEG, or PDF, choose size and background, then share or Save to Photos. Stacked, Scatter, Radar, and Gantt require Pro to export.</p>
      </section>""",
            '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../../">Home</a><span class="crumb-sep" aria-hidden="true">›</span><a href="../">App</a><span class="crumb-sep" aria-hidden="true">›</span><span aria-current="page">Export</span></nav>',
        ),
        "app/supported-chart-types/index.html": (
            "Supported Chart Types in VIA App",
            "Full list of chart types in the VIA chart maker app: pie, donut, line, area, bar, H. Bar, stacked, scatter, radar, gantt — with Pro export notes.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>Which chart types does VIA support?</h2></div>
        <p class="quick-answer">VIA supports ten <strong>chart types</strong> for mobile <strong>data visualization</strong>. Browser chart maker tools cover pie and bar only; the rest are built in the iPhone app.</p>
      </section>""",
            '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../../">Home</a><span class="crumb-sep" aria-hidden="true">›</span><a href="../">App</a><span class="crumb-sep" aria-hidden="true">›</span><span aria-current="page">Supported types</span></nav>',
        ),
        "spider-chart/index.html": (
            "Spider Chart Meaning — Radar in VIA",
            "A spider chart is another name for a radar chart. Learn spider chart data visualization and make one on iPhone in VIA (UI label: Radar). Export needs Pro.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>Is a spider chart the same as a radar chart?</h2></div>
        <p class="quick-answer">Yes in everyday <strong>data visualization</strong>: spider chart, web chart, and radar chart describe the same multi-axis profile. VIA’s chart maker label is <strong>Radar</strong>, not Spider.</p>
      </section>""",
            None,
        ),
        "learn/choose-a-chart-type/index.html": (
            "Choose a Chart Type — Decision Guide",
            "Choose a chart type with clear rules: pie chart, bar chart, line chart, scatter, radar, gantt. Data visualization decisions before you open any chart maker.",
            None,
            None,
        ),
        "learn/glossary/index.html": (
            "Chart Glossary — Data Visualization Terms",
            "Chart glossary for data visualization: chart, graph, legend, axis, series, part-to-whole, baseline, export — terms every chart maker user should know.",
            """
      <section class="section prose keyword-block">
        <div class="section-head"><h2>Why a chart glossary matters</h2></div>
        <p class="quick-answer">Clear vocabulary makes <strong>data visualization</strong> easier to teach and cite. These definitions support students using any chart maker or graph maker.</p>
      </section>""",
            None,
        ),
        "learn/common-chart-mistakes/index.html": (
            "Common Chart Mistakes in Data Viz",
            "Common chart mistakes that hurt data visualization: too many pie slices, truncated bar baselines, wrong chart types, and radar overload — fix them before export.",
            None,
            None,
        ),
        "learn/chart-vs-graph/index.html": (
            "Chart vs Graph — Data Visualization Terms",
            "Chart vs graph explained for data visualization: everyday synonyms for pie charts and bar charts, versus mathematical graphs of nodes and edges.",
            None,
            None,
        ),
    }

    for rel, (title, meta, block, crumb) in hubs.items():
        path = ROOT / rel
        if not path.exists():
            continue
        html = path.read_text()
        # titles may contain &amp; already in file - use plain and let HTML entity if needed
        t = title.replace("&", "&amp;") if "&" in title and "&amp;" not in title else title
        # For set_title_meta we need raw lengths without entities for meta; title displayed may have amp
        # Use unescaped for length checks
        title_plain = title.replace("&amp;", "&")
        meta_plain = meta
        # pad/trim meta
        if len(meta_plain) > 160:
            meta_plain = meta_plain[:157].rstrip() + "…"
        if len(meta_plain) < 140:
            meta_plain = meta_plain + " Free educational guides from VIA."
            meta_plain = meta_plain[:160]
        if len(title_plain) > 60:
            title_plain = title_plain[:57].rstrip() + "…"
        if len(title_plain) < 30:
            title_plain = title_plain + " | VIA Chart Maker"
            title_plain = title_plain[:60]
        html = set_title_meta(html, title_plain, meta_plain)
        if block:
            html = inject_before_faq(html, block)
        if crumb:
            html = ensure_crumb(html, crumb)
        html = ensure_author(html)
        path.write_text(html)
        print("enriched hub", rel)

    # compare articles - add keyword intros if missing
    for c in KG["comparisons"]:
        path = ROOT / "compare" / c["slug"] / "index.html"
        if not path.exists():
            continue
        html = path.read_text()
        if "keyword-block" not in html:
            a = KG["entities"][c["a"]]["label"].lower()
            b = KG["entities"][c["b"]]["label"].lower()
            block = f"""
      <section class="section prose keyword-block">
        <div class="section-head"><h2>Which chart type fits your data visualization?</h2></div>
        <p>Choosing between a <strong>{a} chart</strong> and a <strong>{b} chart</strong> is a common chart maker decision. Use the quick answer and table below, then open the matching free online tool or the VIA graph maker on iPhone.</p>
      </section>"""
            # insert after hero
            html = html.replace("</section>\n\n      <section class=\"section prose answer-block\">", "</section>\n" + block + "\n      <section class=\"section prose answer-block\">", 1)
        html = ensure_author(html)
        # trim long titles
        m = re.search(r"<title>([^<]+)</title>", html)
        if m and len(m.group(1)) > 60:
            short = m.group(1).replace(" — Which Should You Use? | VIA", " | VIA")
            if len(short) > 60:
                short = short[:57] + "…"
            html = set_title_meta(
                html,
                short,
                re.search(r'<meta name="description" content="([^"]*)"', html).group(1)[:160],
            ) if re.search(r'<meta name="description"', html) else html.replace(m.group(0), f"<title>{short}</title>")
        path.write_text(html)
        print("enriched compare", c["slug"])


def main() -> None:
    enrich_types()
    enrich_home()
    enrich_hubs()
    # robots: ensure AI crawlers + sitemap (already open)
    robots = ROOT / "robots.txt"
    txt = robots.read_text()
    if "llms.txt" not in txt:
        robots.write_text(
            txt.rstrip()
            + "\n\n# AI / search helpers\n# llms.txt: https://emilsvetlichnyy.github.io/chart-maker/llms.txt\n# feed: https://emilsvetlichnyy.github.io/chart-maker/feed.xml\n"
        )
    print("done enrich")


if __name__ == "__main__":
    main()
