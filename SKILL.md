# Frontend Slides Skill

A Claude Code skill for creating beautiful, interactive HTML/CSS/JS slide presentations from scratch or by converting PowerPoint files.

## Overview

This skill helps you build presentation slides as web pages with:
- Responsive, viewport-based layouts
- Smooth animations and transitions
- Style presets for consistent theming
- PowerPoint (.pptx) extraction support

## Usage

### Creating a new presentation

Ask Claude to create a slide deck:
```
Create a 10-slide presentation about [topic] using the frontend-slides skill
```

### Converting a PowerPoint

Provide a .pptx file and ask Claude to convert it:
```
Convert my presentation.pptx to an HTML slide deck
```

### Applying a style preset

Reference a preset from STYLE_PRESETS.md:
```
Create slides using the "dark-minimal" preset
```

## File Structure

```
slides/
├── index.html          # Main presentation file
├── style.css           # Custom styles (extends viewport-base.css)
├── animations.css      # Animation classes
└── slides/
    ├── slide-01.html   # Individual slide partials (optional)
    └── ...
```

## Key Principles

1. **Viewport units first** — use `vw`, `vh`, `vmin`, `vmax` for sizing
2. **CSS custom properties** — use variables for theming
3. **Progressive enhancement** — works without JS, enhanced with it
4. **Keyboard navigation** — arrow keys, spacebar always work
5. **Print-friendly** — each slide prints as one page

## Navigation Controls

Generated slides always include:
- Arrow key navigation (← →)
- Spacebar to advance
- Click/tap to advance
- Slide counter display
- Optional presenter notes (press `N`)

## Dependencies

No external dependencies required. All styles and scripts are self-contained.

Optional:
- `scripts/extract-pptx.py` — requires `python-pptx` (`pip install python-pptx`)
