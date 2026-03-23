# HTML Slide Template

This document provides the canonical HTML boilerplate for a frontend slides presentation. Copy and adapt it as a starting point.

## Full Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Presentation Title</title>

  <!-- Google Fonts (choose based on style preset) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">

  <style>
    /* ── 1. Style Preset ──────────────────────────────────────── */
    :root {
      --bg-primary: #0d0d0d;
      --bg-secondary: #1a1a1a;
      --text-primary: #f0f0f0;
      --text-secondary: #a0a0a0;
      --accent: #00e5ff;
      --accent-secondary: #7c4dff;
      --font-heading: 'Inter', system-ui, sans-serif;
      --font-body: 'Inter', system-ui, sans-serif;
      --font-mono: 'SFMono-Regular', monospace;
      --slide-padding: 6vw;
      --heading-size: 5vw;
      --body-size: 2.2vw;
    }

    /* ── 2. Base Styles (inline or link viewport-base.css) ────── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html, body {
      width: 100%; height: 100%; overflow: hidden;
      background: var(--bg-primary); color: var(--text-primary);
      font-family: var(--font-body); font-size: var(--body-size);
      -webkit-font-smoothing: antialiased;
    }

    .slides-wrapper { width: 100vw; height: 100vh; position: relative; overflow: hidden; }

    .slide {
      position: absolute; inset: 0;
      width: 100vw; height: 100vh;
      padding: var(--slide-padding);
      display: flex; flex-direction: column;
      justify-content: center; align-items: flex-start;
      background: var(--bg-primary);
      opacity: 0; pointer-events: none;
      transition: opacity 400ms ease, transform 400ms ease;
      transform: translateX(4vw);
    }
    .slide.active { opacity: 1; pointer-events: all; transform: translateX(0); }
    .slide.prev { transform: translateX(-4vw); }

    h1 { font-size: var(--heading-size); font-weight: 700; line-height: 1.15; letter-spacing: -0.02em; }
    h2 { font-size: calc(var(--heading-size) * 0.65); font-weight: 600; }
    p, li { line-height: 1.6; }
    strong { color: var(--accent); }

    .accent { color: var(--accent); }
    .muted  { color: var(--text-secondary); }
    .divider { width: 6vw; height: 0.4vh; background: var(--accent); margin: 2vh 0; border-radius: 2px; }

    .slide-counter {
      position: fixed; bottom: 2.5vh; right: 2.5vw;
      font-size: 1.3vw; color: var(--text-secondary);
      font-family: var(--font-mono); z-index: 100; user-select: none;
    }
    .progress-bar {
      position: fixed; bottom: 0; left: 0; height: 0.4vh;
      background: var(--accent); transition: width 400ms ease; z-index: 100;
    }

    /* ── 3. Custom Slide Styles ───────────────────────────────── */
    /* Add your slide-specific overrides here */
  </style>
</head>
<body>

<div class="slides-wrapper">

  <!-- ── SLIDE 1: Title ─────────────────────────────────────── -->
  <section class="slide active" id="slide-1">
    <div class="divider"></div>
    <h1>Your Presentation Title</h1>
    <p class="muted" style="margin-top: 3vh; font-size: 2.5vw;">Subtitle or tagline here</p>
    <p class="muted" style="margin-top: 6vh; font-size: 1.6vw;">Author Name · Date</p>
    <aside class="notes">Speaker notes for slide 1 go here.</aside>
  </section>

  <!-- ── SLIDE 2: Agenda / Overview ────────────────────────── -->
  <section class="slide" id="slide-2">
    <h2>Agenda</h2>
    <div class="divider"></div>
    <ol style="margin-top: 3vh; padding-left: 2.5vw; display: flex; flex-direction: column; gap: 2vh;">
      <li>Topic One</li>
      <li>Topic Two</li>
      <li>Topic Three</li>
      <li>Topic Four</li>
    </ol>
    <aside class="notes">Walk through the agenda briefly.</aside>
  </section>

  <!-- ── SLIDE 3: Content Slide ────────────────────────────── -->
  <section class="slide" id="slide-3">
    <h2>Section Title</h2>
    <div class="divider"></div>
    <p style="margin-top: 3vh; max-width: 60vw;">
      Your content goes here. Keep it concise — one key idea per slide.
      Use <strong>emphasis</strong> sparingly.
    </p>
    <aside class="notes">Expand on the key point here.</aside>
  </section>

  <!-- ── SLIDE N: Add more slides above this line ──────────── -->

  <!-- ── SLIDE LAST: Thank You / End ──────────────────────── -->
  <section class="slide" id="slide-end">
    <div class="divider"></div>
    <h1>Thank You</h1>
    <p class="muted" style="margin-top: 3vh;">Questions?</p>
    <p style="margin-top: 6vh; font-size: 1.6vw;" class="accent">your@email.com</p>
    <aside class="notes">Open the floor for Q&A.</aside>
  </section>

</div><!-- /.slides-wrapper -->

<!-- ── UI Chrome ─────────────────────────────────────────────── -->
<div class="slide-counter">
  <span id="current-slide">1</span> / <span id="total-slides"></span>
</div>
<div class="progress-bar" id="progress-bar"></div>

<script>
  (() => {
    const slides = Array.from(document.querySelectorAll('.slide'));
    const counter = document.getElementById('current-slide');
    const total = document.getElementById('total-slides');
    const progressBar = document.getElementById('progress-bar');
    let current = 0;

    total.textContent = slides.length;

    function goTo(index) {
      if (index < 0 || index >= slides.length) return;
      slides[current].classList.remove('active');
      slides[current].classList.add('prev');
      setTimeout(() => slides[current].classList.remove('prev'), 420);
      current = index;
      slides[current].classList.add('active');
      counter.textContent = current + 1;
      progressBar.style.width = ((current + 1) / slides.length * 100) + '%';
    }

    function next() { goTo(current + 1); }
    function prev() { goTo(current - 1); }

    document.addEventListener('keydown', e => {
      if (['ArrowRight', 'ArrowDown', ' '].includes(e.key)) { e.preventDefault(); next(); }
      if (['ArrowLeft', 'ArrowUp'].includes(e.key)) { e.preventDefault(); prev(); }
      if (e.key === 'Home') goTo(0);
      if (e.key === 'End') goTo(slides.length - 1);
    });

    // Click / tap to advance (right half) or go back (left half)
    document.addEventListener('click', e => {
      if (e.clientX > window.innerWidth / 2) next(); else prev();
    });

    // Touch swipe
    let touchStartX = 0;
    document.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
    document.addEventListener('touchend', e => {
      const dx = touchStartX - e.changedTouches[0].clientX;
      if (Math.abs(dx) > 50) { if (dx > 0) next(); else prev(); }
    });

    // Init
    goTo(0);
  })();
</script>

</body>
</html>
```

## Slide Layouts

### Title slide
```html
<section class="slide active" id="slide-title">
  <div class="divider"></div>
  <h1>Title Here</h1>
  <p class="muted" style="margin-top: 2vh; font-size: 2.5vw;">Subtitle</p>
</section>
```

### Two-column split
```html
<section class="slide" id="slide-split">
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4vw; width: 100%;">
    <div>
      <h2>Left Column</h2>
      <p>Content here</p>
    </div>
    <div>
      <h2>Right Column</h2>
      <p>Content here</p>
    </div>
  </div>
</section>
```

### Full-bleed image
```html
<section class="slide" id="slide-image"
  style="padding: 0; background-image: url('image.jpg'); background-size: cover; background-position: center;">
  <div style="position: absolute; inset: 0; background: rgba(0,0,0,0.5);"></div>
  <div style="position: relative; padding: var(--slide-padding);">
    <h1>Overlay Title</h1>
  </div>
</section>
```

### Stats / metrics
```html
<section class="slide" id="slide-stats">
  <h2>By the Numbers</h2>
  <div class="divider"></div>
  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 3vw; margin-top: 4vh; width: 100%;">
    <div style="text-align: center;">
      <div style="font-size: 8vw; font-weight: 700; color: var(--accent);">42%</div>
      <p class="muted">Metric label</p>
    </div>
    <!-- repeat for other stats -->
  </div>
</section>
```

### Code slide
```html
<section class="slide" id="slide-code">
  <h2>Code Example</h2>
  <div class="divider"></div>
  <pre style="margin-top: 3vh; width: 100%;"><code>function hello(name) {
  return `Hello, ${name}!`;
}

console.log(hello('World'));</code></pre>
</section>
```

## Tips

- Aim for **one idea per slide**
- Keep bullet lists to **3–5 items max**
- Use `font-size` with `vw` units everywhere for scaling
- Test at 1280×720, 1920×1080, and on mobile
- Add `id` attributes to every `<section>` for deep-linking
