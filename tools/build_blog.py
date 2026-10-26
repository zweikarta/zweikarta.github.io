#!/usr/bin/env python3
"""Build the blog from Markdown files. No dependencies, Python 3.8+.

    python3 tools/build_blog.py

Reads content/blog/<slug>.md and writes:
  blog/<slug>/index.html   one page per post
  blog/index.html          the list of posts
  blog/feed.xml            RSS feed
  sitemap.xml              blog entries refreshed, other entries kept

A post starts with a front matter block:

    ---
    title: Shown as the H1
    seo_title: Optional, used for <title> and link previews (keep it under 60 characters)
    description: Meta description, 140 to 160 characters
    date: 2026-10-27
    updated: optional, a later date when the post changes
    app: geldspace (optional: adds the app call to action and uses its preview image)
    image: cover.jpg (1200x630, in assets/blog/<slug>/)
    image_alt: Text for the cover image
    draft: true (optional: skipped by the build)
    ---

A closing block about the app goes between `::: app <phone screenshot>` and `:::`. It is
shown as a card in the app's colours with the screenshot and a link to the app page.

The body is a small Markdown subset: ## and ### headings, paragraphs, - and 1. lists,
**bold**, *italic*, [links](url) and images on their own line:

    ![Alt text](file.png "Optional caption")

Image files live in assets/blog/<slug>/. Width and height are read from the file.
"""
import datetime
import html
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://zweikarta.com"
SRC = ROOT / "content" / "blog"
OUT = ROOT / "blog"

APPS = {
    "geldspace": {
        "name": "GeldSpace",
        "url": "/geldspace/",
        "pitch": "Your wealth in one calm place, alone or as a couple. Mine stays private, Ours is shared, and a two-minute monthly check-in keeps it fresh.",
        "cta": "See how GeldSpace works",
        "status": "Coming soon to iPhone and Android.",
    }
}

LOGO = ('<svg viewBox="0 0 34 22" aria-hidden="true"><defs><clipPath id="logo-clip"><circle cx="11" cy="11" r="10"/>'
        '</clipPath></defs><circle cx="11" cy="11" r="10" fill="#3D5AFE"/><circle cx="23" cy="11" r="10" fill="#FFAE2B"/>'
        '<circle class="lens" cx="23" cy="11" r="10" clip-path="url(#logo-clip)"/></svg>')


def css_version():
    # Changes whenever studio.css changes, so browsers never use an old cached copy.
    import hashlib
    return hashlib.sha1((ROOT / "assets" / "studio.css").read_bytes()).hexdigest()[:8]


def esc(s):
    return html.escape(s, quote=True)


def image_size(path):
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    i = 2  # JPEG: walk the segments to the frame header
    while i < len(data):
        marker, length = data[i + 1], struct.unpack(">H", data[i + 2:i + 4])[0]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + length
    raise ValueError(f"unknown image format: {path}")


def picture(slug, src, w, h, alt, sizes, extra=""):
    """An <img>, wrapped in <picture> with WebP sources when tools/optimize_images.py made them."""
    folder = ROOT / "assets" / "blog" / slug
    stem = Path(src).stem
    variants = sorted((int(f.stem.rsplit("-", 1)[1]), f.name) for f in folder.glob(f"{stem}-*.webp")
                      if f.stem.rsplit("-", 1)[1].isdigit())
    img = f'<img src="/assets/blog/{slug}/{src}" width="{w}" height="{h}" alt="{esc(alt)}"{extra}>'
    if not variants:
        return img
    srcset = ", ".join(f"/assets/blog/{slug}/{name} {vw}w" for vw, name in variants)
    return f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">{img}</picture>'


def inline(text):
    text = esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', text)


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def render_body(md, slug):
    out, para, items, list_tag = [], [], [], None
    toc = []
    first_image = True

    def flush():
        nonlocal para, items, list_tag
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para = []
        if items:
            out.append(f"<{list_tag}>" + "".join(f"<li>{inline(i)}</li>" for i in items) + f"</{list_tag}>")
            items, list_tag = [], None

    for line in md.splitlines():
        s = line.strip()
        img = re.fullmatch(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)', s)
        if not s:
            flush()
        elif s.startswith("### ") or s.startswith("## "):
            flush()
            level = 3 if s.startswith("### ") else 2
            title = s[level + 1:]
            hid = slugify(title)
            if level == 2:
                toc.append((hid, title))
            out.append(f'<h{level} id="{hid}">{inline(title)}</h{level}>')
        elif img:
            flush()
            alt, src, caption = img.groups()
            w, h = image_size(ROOT / "assets" / "blog" / slug / src)
            loading = "" if first_image else ' loading="lazy"'
            first_image = False
            sizes = "250px" if h > w else "(max-width: 46rem) 100vw, 736px"
            fig = picture(slug, src, w, h, alt, sizes, f'{loading} decoding="async"')
            if caption:
                fig += f"<figcaption>{inline(caption)}</figcaption>"
            out.append(f'<figure class="{"phone" if h > w else "wide"}">{fig}</figure>')
        elif re.match(r"^(- |\d+\. )", s):
            if para:
                flush()
            tag = "ul" if s.startswith("- ") else "ol"
            if list_tag and list_tag != tag:
                flush()
            list_tag = tag
            items.append(re.sub(r"^(- |\d+\. )", "", s))
        else:
            if items:
                flush()
            para.append(s)
    flush()
    return "\n".join(out), toc


def parse(path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    meta["slug"] = path.stem
    meta["body"] = m.group(2)
    meta.setdefault("seo_title", meta["title"])
    meta.setdefault("updated", meta["date"])
    return meta


def nice_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def head(title, description, url, image, image_alt, og_type, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Zweikarta">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(image_alt)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="Zweikarta blog" href="{SITE}/blog/feed.xml">
{extra}<link rel="icon" href="/assets/mark.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/bricolage-grotesque-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/studio.css?v={css_version()}">
<script src="/assets/consent.js" defer></script>
</head>
<body class="blog-page">

<header class="blog-top">
  <div class="wrap topbar">
    <a class="logo" href="/" aria-label="Zweikarta home">
      {LOGO}
      zweikarta
    </a>
    <nav aria-label="Main">
      <a href="/#apps">Apps</a>
      <a href="/geldspace/" class="hide-sm">GeldSpace</a>
      <a href="/blog/" aria-current="{'page' if url.endswith('/blog/') else 'false'}">Blog</a>
    </nav>
  </div>
</header>
"""


FOOT = """
<footer class="foot">
  <div class="wrap">
    <span>© 2026 Zweikarta · Berlin</span>
    <nav aria-label="Legal"><a href="/imprint/">Imprint</a><a href="/privacy/">Website privacy</a><a href="/geldspace/privacy/">GeldSpace privacy</a></nav>
  </div>
</footer>
</body>
</html>
"""


def ld(obj):
    import json
    return '<script type="application/ld+json">\n' + json.dumps(obj, indent=2, ensure_ascii=False) + "\n</script>\n"


def build_post(p):
    slug = p["slug"]
    url = f"{SITE}/blog/{slug}/"
    image = f"{SITE}/assets/blog/{slug}/{p['image']}"
    app = APPS.get(p.get("app", ""))
    app_block = ""
    m = re.search(r"^::: app (\S+)\n(.*?)^:::$", p["body"], re.S | re.M)
    md = p["body"]
    if m:
        inner, inner_toc = render_body(m.group(2), slug)
        src = m.group(1)
        w, h = image_size(ROOT / "assets" / "blog" / slug / src)
        app_block = f"""
  <aside class="post-app" aria-label="{app['name']}">
    <div class="post-app-copy">
{inner}
      <a class="btn btn-light" href="{app['url']}">{esc(app['cta'])}</a>
      <p class="post-app-note">{esc(app['status'])}</p>
    </div>
    {picture(slug, src, w, h, app['name'] + " on a phone", "250px", ' loading="lazy" decoding="async"')}
  </aside>"""
        md = p["body"][:m.start()] + p["body"][m.end():]
    body, toc = render_body(md, slug)
    if m:
        toc += inner_toc
    words = len(re.findall(r"\w+", p["body"]))
    minutes = max(1, round(words / 220))
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "@id": url + "#post",
                "headline": p["seo_title"],
                "description": p["description"],
                "image": image,
                "datePublished": p["date"],
                "dateModified": p["updated"],
                "inLanguage": "en",
                "wordCount": words,
                "mainEntityOfPage": url,
                "author": {"@type": "Organization", "@id": f"{SITE}/#org", "name": "Zweikarta", "url": f"{SITE}/"},
                "publisher": {"@type": "Organization", "@id": f"{SITE}/#org", "name": "Zweikarta",
                              "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/mark.svg"}},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Zweikarta", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog/"},
                    {"@type": "ListItem", "position": 3, "name": p["title"], "item": url},
                ],
            },
        ],
    }
    extra = (f'<meta property="article:published_time" content="{p["date"]}">\n'
             f'<meta property="article:modified_time" content="{p["updated"]}">\n' + ld(schema))
    toc_html = "".join(f'<li><a href="#{i}">{inline(t)}</a></li>' for i, t in toc)
    cta = app_block
    if app and not app_block:
        cta = f"""
  <aside class="post-cta" aria-label="{app['name']}">
    <p class="kicker">From the makers of this blog</p>
    <h2>{app['name']}</h2>
    <p>{esc(app['pitch'])}</p>
    <a class="btn btn-light" href="{app['url']}">{esc(app['cta'])}</a>
    <p class="post-cta-note">{esc(app['status'])}</p>
  </aside>"""
    page = head(f"{p['seo_title']} · Zweikarta", p["description"], url, image, p["image_alt"], "article", extra)
    page += f"""
<main>
<article class="post wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/blog/">Blog</a></nav>
  <h1>{inline(p['title'])}</h1>
  <p class="post-meta"><time datetime="{p['date']}">{nice_date(p['date'])}</time> · {minutes} min read · By Zweikarta</p>
  <figure class="post-cover">{picture(slug, p['image'], 1200, 630, p['image_alt'], "(max-width: 46rem) 100vw, 736px", ' fetchpriority="high"')}</figure>
  <nav class="post-toc" aria-label="In this post"><p class="kicker">In this post</p><ol>{toc_html}</ol></nav>
  <div class="post-body">
{body}
  </div>{cta}
  <p class="post-disclaimer">We don't give financial advice. This post shares ideas and conversation starters, not recommendations for your situation.</p>
</article>
</main>
"""
    page += FOOT
    (OUT / slug).mkdir(parents=True, exist_ok=True)
    (OUT / slug / "index.html").write_text(page, encoding="utf-8")


def build_index(posts):
    url = f"{SITE}/blog/"
    desc = "Notes from Zweikarta, a two-person app studio in Berlin: money as a couple, calm apps, and what we learn building GeldSpace."
    schema = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "@id": url + "#blog",
        "name": "Zweikarta blog",
        "url": url,
        "description": desc,
        "publisher": {"@id": f"{SITE}/#org"},
        "inLanguage": "en",
        "blogPost": [{"@type": "BlogPosting", "headline": p["seo_title"], "url": f"{SITE}/blog/{p['slug']}/",
                      "datePublished": p["date"]} for p in posts],
    }
    cards = "".join(f"""
    <li class="post-card">
      <a href="/blog/{p['slug']}/">
        {picture(p['slug'], p['image'], 1200, 630, "", "(max-width: 760px) 100vw, 400px", ' loading="lazy" decoding="async"')}
        <span class="post-card-text">
          <time datetime="{p['date']}">{nice_date(p['date'])}</time>
          <strong>{inline(p['title'])}</strong>
          <span>{esc(p['description'])}</span>
        </span>
      </a>
    </li>""" for p in posts)
    page = head("Blog · Zweikarta", desc, url, f"{SITE}/assets/og/studio.jpg",
                "Zweikarta: two makers, one studio. Independent app studio in Berlin.", "website", ld(schema))
    page += f"""
<main>
<section class="blog-list wrap">
  <p class="kicker">Blog</p>
  <h1>Money, couples and calm apps.</h1>
  <p class="lede">Short, practical notes from the two of us at Zweikarta, and what we learn building GeldSpace.</p>
  <ul class="post-cards">{cards}
  </ul>
</section>
</main>
"""
    page += FOOT
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(page, encoding="utf-8")


def build_feed(posts):
    items = "".join(f"""
  <item>
    <title>{esc(p['seo_title'])}</title>
    <link>{SITE}/blog/{p['slug']}/</link>
    <guid>{SITE}/blog/{p['slug']}/</guid>
    <pubDate>{datetime.datetime.fromisoformat(p['date'] + 'T08:00:00+00:00').strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
    <description>{esc(p['description'])}</description>
  </item>""" for p in posts)
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Zweikarta blog</title>
  <link>{SITE}/blog/</link>
  <atom:link href="{SITE}/blog/feed.xml" rel="self" type="application/rss+xml"/>
  <description>Money, couples and calm apps, from the makers of GeldSpace.</description>
  <language>en</language>{items}
</channel>
</rss>
"""
    (OUT / "feed.xml").write_text(feed, encoding="utf-8")


def update_sitemap(posts):
    path = ROOT / "sitemap.xml"
    lines = [l for l in path.read_text(encoding="utf-8").splitlines() if "/blog/" not in l]
    newest = max(p["updated"] for p in posts)
    entries = [f"  <url><loc>{SITE}/blog/</loc><lastmod>{newest}</lastmod></url>"]
    entries += [f"  <url><loc>{SITE}/blog/{p['slug']}/</loc><lastmod>{p['updated']}</lastmod></url>" for p in posts]
    end = lines.index("</urlset>")
    path.write_text("\n".join(lines[:end] + entries + lines[end:]) + "\n", encoding="utf-8")


def main():
    posts = [parse(f) for f in sorted(SRC.glob("*.md"))]
    posts = sorted((p for p in posts if p.get("draft") != "true"), key=lambda p: p["date"], reverse=True)
    for p in posts:
        build_post(p)
    build_index(posts)
    build_feed(posts)
    update_sitemap(posts)
    print(f"Built {len(posts)} post(s).")


if __name__ == "__main__":
    main()
