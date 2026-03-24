# Frontend Slides Skill

Base directory for this skill: /root/.claude/skills/frontend-slides

You are now in **frontend-slides mode**. Your job is to create a beautiful, self-contained HTML slide presentation.

---

## What to do

1. **Understand the request** — determine topic, number of slides, and preferred style preset (default: `dark-minimal`).
2. **Read the reference files** from the skill base directory:
   - `STYLE_PRESETS.md` — choose or apply a CSS theme
   - `html-template.md` — use the canonical HTML boilerplate
   - `animation-patterns.md` — pick appropriate entry animations
   - `viewport-base.css` — inline or link for base styles
3. **Generate** a single self-contained `index.html` file (or the filename requested).
4. **Write** the file to the current working directory.

---

## Rules

- Every size value uses viewport units (`vw`, `vh`, `vmin`) — never `px` for layout.
- CSS custom properties (`var(--...)`) control all colors, fonts, and spacing.
- Navigation is always included: arrow keys, spacebar, click/tap, swipe.
- Slide counter and progress bar are always present.
- Speaker notes go in `<aside class="notes">` (hidden by default).
- `prefers-reduced-motion` is always respected.
- No external JS dependencies. Fonts from Google Fonts are allowed.
- One key idea per slide. Bullet lists max 5 items.

---

## Slide count guidance

| Request | Slides |
|---------|--------|
| "short" / "quick" | 5–7 |
| default / unspecified | 8–12 |
| "detailed" / "full" | 12–20 |

---

## Workflow

### New presentation from scratch

1. Read `html-template.md` and `STYLE_PRESETS.md`.
2. Pick the style preset that fits the topic (or use what the user specified).
3. Outline the slides: title → agenda → content slides → closing.
4. Write the complete `index.html`.

### Convert a PowerPoint

1. Run `python /root/.claude/skills/frontend-slides/scripts/extract-pptx.py <file.pptx>` to get a base HTML file.
2. Read the output HTML.
3. Improve layout, apply a style preset, and add animations.
4. Write the improved file back.

### Restyle existing slides

1. Read the existing HTML file.
2. Apply the requested preset variables from `STYLE_PRESETS.md`.
3. Write the updated file.

---

## Output checklist

Before writing the file, confirm:
- [ ] Style preset variables are defined in `:root`
- [ ] All slides have `id="slide-N"` attributes
- [ ] First slide has `class="slide active"`
- [ ] Navigation JS is included and functional
- [ ] Slide counter and progress bar are present
- [ ] `<aside class="notes">` on every slide
- [ ] No hardcoded `px` sizes for layout elements

---

Now read the necessary reference files and proceed with the user's request.
