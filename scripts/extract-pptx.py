#!/usr/bin/env python3
"""
extract-pptx.py
Extract content from a PowerPoint (.pptx) file and generate an HTML slide deck.

Usage:
    python scripts/extract-pptx.py presentation.pptx [output.html]

Requirements:
    pip install python-pptx

Output:
    A self-contained HTML file using the frontend-slides conventions
    (viewport units, CSS custom properties, keyboard navigation).
"""

import sys
import os
import html
import argparse
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
except ImportError:
    print("Error: python-pptx is required. Install it with:")
    print("    pip install python-pptx")
    sys.exit(1)


# ── Helpers ──────────────────────────────────────────────────────────────────

def rgb_to_hex(color):
    """Convert pptx RGBColor to CSS hex string."""
    if color is None:
        return None
    return f"#{color.rgb:06x}"


def extract_text_runs(paragraph):
    """Extract styled runs from a paragraph as HTML spans."""
    parts = []
    for run in paragraph.runs:
        text = html.escape(run.text or "")
        if not text:
            continue

        styles = []
        if run.font.bold:
            styles.append("font-weight:700")
        if run.font.italic:
            styles.append("font-style:italic")
        if run.font.underline:
            styles.append("text-decoration:underline")
        if run.font.color and run.font.color.type is not None:
            try:
                color = rgb_to_hex(run.font.color.rgb)
                if color:
                    styles.append(f"color:{color}")
            except Exception:
                pass

        if styles:
            parts.append(f'<span style="{"; ".join(styles)}">{text}</span>')
        else:
            parts.append(text)

    return "".join(parts)


def paragraph_to_html(paragraph, is_title=False):
    """Convert a pptx paragraph to an HTML element."""
    text = extract_text_runs(paragraph)
    if not text.strip():
        return ""

    tag = "h1" if is_title else "p"
    align = ""
    if paragraph.alignment == PP_ALIGN.CENTER:
        align = " style=\"text-align:center\""
    elif paragraph.alignment == PP_ALIGN.RIGHT:
        align = " style=\"text-align:right\""

    return f"<{tag}{align}>{text}</{tag}>"


def shape_to_html(shape, shape_index):
    """Convert a pptx shape to HTML content."""
    if not shape.has_text_frame:
        return f"<!-- shape {shape_index}: no text (type: {shape.shape_type}) -->"

    lines = []
    is_first = True
    for para in shape.text_frame.paragraphs:
        line = paragraph_to_html(para, is_title=(is_first and shape_index == 0))
        if line:
            lines.append(line)
        is_first = False

    return "\n    ".join(lines)


def slide_to_html(slide, slide_num, total):
    """Convert a pptx slide to an HTML <section>."""
    content_parts = []

    for i, shape in enumerate(slide.shapes):
        fragment = shape_to_html(shape, i)
        if fragment:
            content_parts.append(fragment)

    content = "\n    ".join(content_parts) if content_parts else "<p class=\"muted\">(empty slide)</p>"

    active_class = " active" if slide_num == 1 else ""
    return f"""  <section class="slide{active_class}" id="slide-{slide_num}">
    {content}
    <aside class="notes"><!-- Add speaker notes here --></aside>
  </section>"""


# ── Main ─────────────────────────────────────────────────────────────────────

HTML_WRAPPER = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    /* ── Style Preset: dark-minimal ───────────────── */
    :root {{
      --bg-primary: #0d0d0d;
      --bg-secondary: #1a1a1a;
      --text-primary: #f0f0f0;
      --text-secondary: #a0a0a0;
      --accent: #00e5ff;
      --font-heading: system-ui, sans-serif;
      --font-body: system-ui, sans-serif;
      --font-mono: 'SFMono-Regular', monospace;
      --slide-padding: 6vw;
      --heading-size: 5vw;
      --body-size: 2.2vw;
    }}

    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    html, body {{
      width: 100%; height: 100%; overflow: hidden;
      background: var(--bg-primary); color: var(--text-primary);
      font-family: var(--font-body); font-size: var(--body-size);
      -webkit-font-smoothing: antialiased;
    }}

    .slides-wrapper {{ width: 100vw; height: 100vh; position: relative; overflow: hidden; }}

    .slide {{
      position: absolute; inset: 0;
      width: 100vw; height: 100vh;
      padding: var(--slide-padding);
      display: flex; flex-direction: column;
      justify-content: center; align-items: flex-start;
      background: var(--bg-primary);
      opacity: 0; pointer-events: none;
      transition: opacity 400ms ease, transform 400ms ease;
      transform: translateX(4vw);
    }}
    .slide.active {{ opacity: 1; pointer-events: all; transform: translateX(0); }}
    .slide.prev   {{ transform: translateX(-4vw); }}

    h1 {{ font-size: var(--heading-size); font-weight: 700; line-height: 1.15; letter-spacing: -0.02em; margin-bottom: 2vh; }}
    h2 {{ font-size: calc(var(--heading-size) * 0.65); font-weight: 600; margin-bottom: 1.5vh; }}
    p  {{ line-height: 1.6; margin-bottom: 1.5vh; }}
    strong {{ color: var(--accent); }}

    .muted {{ color: var(--text-secondary); }}
    .notes {{ display: none; }}

    .slide-counter {{
      position: fixed; bottom: 2.5vh; right: 2.5vw;
      font-size: 1.3vw; color: var(--text-secondary);
      font-family: var(--font-mono); z-index: 100; user-select: none;
    }}
    .progress-bar {{
      position: fixed; bottom: 0; left: 0; height: 0.4vh;
      background: var(--accent); transition: width 400ms ease; z-index: 100;
    }}

    @media (prefers-reduced-motion: reduce) {{
      .slide {{ transition: none; }}
    }}
  </style>
</head>
<body>

<div class="slides-wrapper">

{slides}

</div>

<div class="slide-counter">
  <span id="current-slide">1</span> / <span id="total-slides"></span>
</div>
<div class="progress-bar" id="progress-bar"></div>

<script>
  (() => {{
    const slides = Array.from(document.querySelectorAll('.slide'));
    const counter = document.getElementById('current-slide');
    const total = document.getElementById('total-slides');
    const progressBar = document.getElementById('progress-bar');
    let current = 0;

    total.textContent = slides.length;

    function goTo(index) {{
      if (index < 0 || index >= slides.length) return;
      slides[current].classList.remove('active');
      slides[current].classList.add('prev');
      setTimeout(() => slides[current].classList.remove('prev'), 420);
      current = index;
      slides[current].classList.add('active');
      counter.textContent = current + 1;
      progressBar.style.width = ((current + 1) / slides.length * 100) + '%';
    }}

    document.addEventListener('keydown', e => {{
      if (['ArrowRight', 'ArrowDown', ' '].includes(e.key)) {{ e.preventDefault(); goTo(current + 1); }}
      if (['ArrowLeft', 'ArrowUp'].includes(e.key)) {{ e.preventDefault(); goTo(current - 1); }}
      if (e.key === 'Home') goTo(0);
      if (e.key === 'End') goTo(slides.length - 1);
    }});

    document.addEventListener('click', e => {{
      if (e.clientX > window.innerWidth / 2) goTo(current + 1); else goTo(current - 1);
    }});

    let touchStartX = 0;
    document.addEventListener('touchstart', e => {{ touchStartX = e.touches[0].clientX; }}, {{ passive: true }});
    document.addEventListener('touchend', e => {{
      const dx = touchStartX - e.changedTouches[0].clientX;
      if (Math.abs(dx) > 50) {{ if (dx > 0) goTo(current + 1); else goTo(current - 1); }}
    }});

    goTo(0);
  }})();
</script>

</body>
</html>
"""


def extract(pptx_path: Path, output_path: Path):
    prs = Presentation(str(pptx_path))
    total = len(prs.slides)
    print(f"Found {total} slide(s) in {pptx_path.name}")

    slide_sections = []
    for i, slide in enumerate(prs.slides, start=1):
        print(f"  Processing slide {i}/{total}...")
        slide_sections.append(slide_to_html(slide, i, total))

    # Attempt to extract a title from the first slide
    title = pptx_path.stem
    if prs.slides:
        first = prs.slides[0]
        for shape in first.shapes:
            if shape.has_text_frame and shape.text_frame.text.strip():
                title = shape.text_frame.text.strip()[:80]
                break

    html_content = HTML_WRAPPER.format(
        title=html.escape(title),
        slides="\n\n".join(slide_sections),
    )

    output_path.write_text(html_content, encoding="utf-8")
    print(f"\nDone! Saved to: {output_path}")
    print("Open in a browser and use arrow keys to navigate.")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a PowerPoint (.pptx) file to an HTML slide deck."
    )
    parser.add_argument("input", help="Path to the .pptx file")
    parser.add_argument(
        "output",
        nargs="?",
        help="Output HTML file (default: <input-stem>.html)",
    )
    args = parser.parse_args()

    pptx_path = Path(args.input).resolve()
    if not pptx_path.exists():
        print(f"Error: File not found: {pptx_path}")
        sys.exit(1)
    if pptx_path.suffix.lower() != ".pptx":
        print(f"Warning: Expected a .pptx file, got: {pptx_path.suffix}")

    output_path = Path(args.output).resolve() if args.output else pptx_path.with_suffix(".html")
    extract(pptx_path, output_path)


if __name__ == "__main__":
    main()
