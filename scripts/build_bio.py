#!/usr/bin/env python3
"""Generate light/dark variants of the profile bio SVG.

Stdlib only. Pulls the latest Medium post title via RSS; falls back to '—'
on any network or parse failure so the workflow stays green.
"""

from __future__ import annotations

import datetime as dt
import html
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Final
from xml.sax.saxutils import escape

REPO_ROOT: Final = Path(__file__).resolve().parent.parent
OUT_DIR:   Final = REPO_ROOT / "assets"
MEDIUM_FEED_URL: Final = "https://medium.com/feed/@indugapallignaneswara"


def fetch_latest_post_title() -> str | None:
    """Return the title of the latest Medium post, or None on any failure."""
    try:
        req = urllib.request.Request(
            MEDIUM_FEED_URL,
            headers={"User-Agent": "github-actions profile-readme generator"},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            xml_text = r.read().decode("utf-8", errors="ignore")
        root = ET.fromstring(xml_text)
        for item in root.iter("item"):
            title_elem = item.find("title")
            if title_elem is not None and title_elem.text:
                raw = html.unescape(title_elem.text).strip()
                clean = re.sub(r"<[^>]+>", "", raw).strip()
                if clean:
                    return clean
        return None
    except Exception:
        return None


def truncate(s: str, n: int) -> str:
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


SVG_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 380" width="720" height="380" role="img" aria-label="Gnaneswara Indugapalli — bio">
  <style><![CDATA[
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, 'Cascadia Mono', 'Roboto Mono', monospace; }}
    .bg       {{ fill: {bg}; }}
    .name     {{ fill: {fg};     font-size: 28px; font-weight: 700; letter-spacing: 0.4px; }}
    .role     {{ fill: {fg_dim}; font-size: 13px; }}
    .tag      {{ fill: {accent}; font-size: 14px; font-style: italic; }}
    .label    {{ fill: {fg_dim}; font-size: 10.5px; letter-spacing: 2px; }}
    .value    {{ fill: {fg};     font-size: 13px; }}
    .value-em {{ fill: {fg};     font-size: 13px; font-style: italic; }}
    .meta     {{ fill: {fg_dim}; font-size: 10px; letter-spacing: 0.5px; }}
    .rule     {{ stroke: {rule}; stroke-width: 1; }}
    .dot      {{ fill: {accent}; animation: pulse 2.4s ease-in-out infinite; }}
    @keyframes pulse {{
      0%, 100% {{ opacity: 0.35; }}
      50%      {{ opacity: 1.0; }}
    }}
  ]]></style>

  <rect class="bg" width="720" height="380" rx="12" ry="12"/>

  <!-- header -->
  <text class="name" x="40" y="62">gnaneswara indugapalli</text>
  <text class="role" x="40" y="84">ai engineer  ·  bangalore</text>
  <text class="tag"  x="40" y="118">long horizon  ·  short sprints</text>

  <line class="rule" x1="40" y1="146" x2="680" y2="146"/>

  <!-- shipping -->
  <text class="label" x="40"  y="178">SHIPPING</text>
  <text class="value" x="180" y="178">vision-language systems</text>
  <text class="value" x="180" y="198">multi-agent infrastructure</text>
  <text class="value" x="180" y="218">reinforcement learning environments</text>

  <!-- writing -->
  <text class="label"    x="40"  y="256">WRITING</text>
  <text class="value-em" x="180" y="256">{post_title}</text>

  <line class="rule" x1="40" y1="296" x2="680" y2="296"/>

  <!-- footer -->
  <circle class="dot" cx="46" cy="336" r="4"/>
  <text class="meta" x="60" y="340">synced {synced}  ·  build {build}</text>
</svg>
"""


LIGHT = {
    "bg":     "#fafaf9",
    "fg":     "#0c0a09",
    "fg_dim": "#57534e",
    "accent": "#7c3aed",
    "rule":   "#e7e5e4",
}

DARK = {
    "bg":     "#0c0a09",
    "fg":     "#fafaf9",
    "fg_dim": "#a8a29e",
    "accent": "#a855f7",
    "rule":   "#292524",
}


def render(theme: dict[str, str], post_title: str, synced: str, build: str) -> str:
    safe_title = escape(post_title)
    return SVG_TEMPLATE.format(
        post_title=safe_title, synced=synced, build=build, **theme,
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_title  = fetch_latest_post_title() or "—"
    post_title = truncate(raw_title, 56)

    now    = dt.datetime.now(dt.UTC)
    synced = now.strftime("%Y-%m-%d")

    run_num = os.environ.get("GITHUB_RUN_NUMBER")
    if run_num and run_num.isdigit():
        build = f"#{int(run_num):04d}"
    else:
        build = now.strftime("%y.%m.%d")

    (OUT_DIR / "bio-light.svg").write_text(
        render(LIGHT, post_title, synced, build), encoding="utf-8",
    )
    (OUT_DIR / "bio-dark.svg").write_text(
        render(DARK, post_title, synced, build), encoding="utf-8",
    )

    print(f"wrote {OUT_DIR / 'bio-light.svg'}")
    print(f"wrote {OUT_DIR / 'bio-dark.svg'}")
    print(f"  post:   {post_title}")
    print(f"  synced: {synced}")
    print(f"  build:  {build}")


if __name__ == "__main__":
    main()
