#!/usr/bin/env python3
"""
Fetches the latest legal news from Bar and Bench, LiveLaw and SCC Online Blog
and writes news.json for the SVS Law Offices website.

Only headline + short summary + link are stored. Full articles are never
copied; every item links out to the publisher's own page.

Run weekly by .github/workflows/update-news.yml
"""

import json, re, sys, html, datetime, urllib.request, urllib.error
from xml.etree import ElementTree as ET

# Candidate feed URLs per source. The first one that returns usable items wins.
SOURCES = [
    ("Bar and Bench", [
        "https://www.barandbench.com/feed",
        "https://www.barandbench.com/rss",
        "https://www.barandbench.com/stories.rss",
    ]),
    ("LiveLaw", [
        "https://www.livelaw.in/rss/latest-news",
        "https://www.livelaw.in/rss/top-stories",
        "https://www.livelaw.in/rss",
    ]),
    ("SCC Online", [
        "https://www.scconline.com/blog/feed/",
        "https://www.scconline.com/blog/rss",
    ]),
]

PER_SOURCE = 4          # items to take from each publication
SUMMARY_WORDS = 28      # keep summaries short; these are pointers, not reproductions
UA = "Mozilla/5.0 (compatible; SVSLawOfficesBot/1.0; +https://svslawoffices.in)"


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/rss+xml, application/xml, text/xml, */*",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def strip_html(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def shorten(text, words=SUMMARY_WORDS):
    """Trim to a short pointer. Never reproduce a full article."""
    t = strip_html(text)
    if not t:
        return ""
    parts = t.split()
    if len(parts) <= words:
        return t
    return " ".join(parts[:words]).rstrip(",;:.") + "\u2026"


def parse_date(raw):
    if not raw:
        return None, ""
    raw = raw.strip()
    fmts = ["%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z",
            "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S"]
    for f in fmts:
        try:
            dt = datetime.datetime.strptime(raw.replace("GMT", "+0000"), f)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=datetime.timezone.utc)
            return dt, dt.strftime("%d %b %Y")
        except ValueError:
            continue
    return None, ""


def parse_feed(xml_bytes):
    """Handle both RSS 2.0 and Atom."""
    root = ET.fromstring(xml_bytes)
    ns = {"atom": "http://www.w3.org/2005/Atom",
          "content": "http://purl.org/rss/1.0/modules/content/"}
    out = []

    entries = root.findall(".//item")
    if entries:  # RSS
        for it in entries:
            title = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            desc = it.findtext("description") or ""
            pub = it.findtext("pubDate") or ""
            if title and link:
                out.append((title, link, desc, pub))
        return out

    for it in root.findall("atom:entry", ns):  # Atom
        title = (it.findtext("atom:title", default="", namespaces=ns) or "").strip()
        link_el = it.find("atom:link", ns)
        link = link_el.get("href").strip() if link_el is not None and link_el.get("href") else ""
        desc = (it.findtext("atom:summary", default="", namespaces=ns)
                or it.findtext("atom:content", default="", namespaces=ns) or "")
        pub = (it.findtext("atom:updated", default="", namespaces=ns)
               or it.findtext("atom:published", default="", namespaces=ns) or "")
        if title and link:
            out.append((title, link, desc, pub))
    return out


def collect():
    items = []
    for source, urls in SOURCES:
        got = False
        for url in urls:
            try:
                raw = parse_feed(fetch(url))
            except Exception as e:
                print(f"  [skip] {url}: {e}", file=sys.stderr)
                continue
            if not raw:
                continue

            taken = 0
            for title, link, desc, pub in raw:
                if taken >= PER_SOURCE:
                    break
                dt, nice = parse_date(pub)
                items.append({
                    "source": source,
                    "title": strip_html(title)[:150],
                    "summary": shorten(desc),
                    "link": link,
                    "date": nice,
                    "_sort": dt.timestamp() if dt else 0,
                })
                taken += 1

            if taken:
                print(f"  [ok] {source}: {taken} items from {url}")
                got = True
                break

        if not got:
            print(f"  [warn] {source}: no feed reachable", file=sys.stderr)

    items.sort(key=lambda x: x["_sort"], reverse=True)
    for i in items:
        i.pop("_sort", None)
    return items


def main():
    print("Fetching legal news feeds...")
    items = collect()

    if not items:
        # Never overwrite a good file with an empty one; keep the last known feed.
        print("No items fetched. Leaving existing news.json untouched.", file=sys.stderr)
        return 1

    payload = {
        "updated": datetime.datetime.now(datetime.timezone.utc)
                    .isoformat(timespec="seconds").replace("+00:00", "Z"),
        "items": items,
    }
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Wrote news.json with {len(items)} items.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
