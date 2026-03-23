# Animation Patterns

CSS and JS animation patterns for frontend slide presentations. All animations are viewport-unit aware and respect `prefers-reduced-motion`.

---

## Reduced Motion First

Always wrap animations in a motion media query. Include this at the top of your styles:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Slide Transitions

### Default: Slide + Fade (built into viewport-base.css)

```css
.slide {
  opacity: 0;
  transform: translateX(4vw);
  transition: opacity 400ms cubic-bezier(0.4, 0, 0.2, 1),
              transform 400ms cubic-bezier(0.4, 0, 0.2, 1);
}
.slide.active { opacity: 1; transform: translateX(0); }
.slide.prev   { transform: translateX(-4vw); }
```

### Fade Only

```css
.slide {
  opacity: 0;
  transition: opacity 500ms ease;
}
.slide.active { opacity: 1; }
```

### Scale Up (zoom in)

```css
.slide {
  opacity: 0;
  transform: scale(0.96);
  transition: opacity 400ms ease, transform 400ms ease;
}
.slide.active { opacity: 1; transform: scale(1); }
```

### Vertical Scroll

```css
.slide {
  opacity: 0;
  transform: translateY(4vh);
  transition: opacity 400ms ease, transform 400ms ease;
}
.slide.active { opacity: 1; transform: translateY(0); }
.slide.prev   { transform: translateY(-4vh); }
```

---

## Element Entry Animations

Use these on individual elements within a slide. Trigger by adding the class when the slide becomes active (see JS helpers below).

### Fade Up

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(2vh); }
  to   { opacity: 1; transform: translateY(0); }
}

.anim-fade-up {
  animation: fadeUp 500ms cubic-bezier(0.4, 0, 0.2, 1) both;
}
```

### Fade In

```css
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

.anim-fade-in {
  animation: fadeIn 500ms ease both;
}
```

### Slide In from Left

```css
@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-4vw); }
  to   { opacity: 1; transform: translateX(0); }
}

.anim-slide-left {
  animation: slideInLeft 500ms cubic-bezier(0.4, 0, 0.2, 1) both;
}
```

### Slide In from Right

```css
@keyframes slideInRight {
  from { opacity: 0; transform: translateX(4vw); }
  to   { opacity: 1; transform: translateX(0); }
}

.anim-slide-right {
  animation: slideInRight 500ms cubic-bezier(0.4, 0, 0.2, 1) both;
}
```

### Scale In (pop)

```css
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.8); }
  to   { opacity: 1; transform: scale(1); }
}

.anim-scale-in {
  animation: scaleIn 400ms cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
```

### Typewriter (text reveal)

```css
@keyframes typewriter {
  from { width: 0; }
  to   { width: 100%; }
}

.anim-typewriter {
  overflow: hidden;
  white-space: nowrap;
  border-right: 0.15em solid var(--accent);
  animation: typewriter 2s steps(40) both,
             blink 0.75s step-end infinite;
  width: fit-content;
}

@keyframes blink {
  50% { border-color: transparent; }
}
```

### Underline Draw

```css
.anim-underline {
  position: relative;
  display: inline-block;
}

.anim-underline::after {
  content: '';
  position: absolute;
  bottom: -0.2em;
  left: 0;
  width: 0;
  height: 0.15em;
  background: var(--accent);
  transition: width 600ms cubic-bezier(0.4, 0, 0.2, 1);
}

.slide.active .anim-underline::after {
  width: 100%;
}
```

---

## Stagger Delays

Apply stagger to a list of elements so they animate in sequence:

```css
/* CSS approach */
.stagger > *:nth-child(1) { animation-delay: 0ms; }
.stagger > *:nth-child(2) { animation-delay: 100ms; }
.stagger > *:nth-child(3) { animation-delay: 200ms; }
.stagger > *:nth-child(4) { animation-delay: 300ms; }
.stagger > *:nth-child(5) { animation-delay: 400ms; }
.stagger > *:nth-child(6) { animation-delay: 500ms; }
```

```html
<ul class="stagger">
  <li class="anim-fade-up">Item 1</li>
  <li class="anim-fade-up">Item 2</li>
  <li class="anim-fade-up">Item 3</li>
</ul>
```

Or apply dynamically with JS:

```js
function staggerChildren(parent, delay = 100) {
  Array.from(parent.children).forEach((child, i) => {
    child.style.animationDelay = `${i * delay}ms`;
  });
}
```

---

## Progress / Counter Animations

### Animated number counter

```js
function animateCounter(el, target, duration = 1500) {
  const start = performance.now();
  const initial = 0;

  function update(time) {
    const elapsed = time - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    el.textContent = Math.round(initial + (target - initial) * eased);
    if (progress < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}

// Usage: <span data-count="42"></span>
document.querySelectorAll('[data-count]').forEach(el => {
  animateCounter(el, parseInt(el.dataset.count));
});
```

### Circular progress ring

```html
<svg class="progress-ring" width="10vw" height="10vw" viewBox="0 0 100 100">
  <circle class="ring-bg" cx="50" cy="50" r="42"
    fill="none" stroke="var(--surface-border)" stroke-width="8"/>
  <circle class="ring-fill" cx="50" cy="50" r="42"
    fill="none" stroke="var(--accent)" stroke-width="8"
    stroke-dasharray="264" stroke-dashoffset="264"
    stroke-linecap="round" transform="rotate(-90 50 50)"/>
  <text x="50" y="55" text-anchor="middle" font-size="24"
    fill="var(--text-primary)" font-family="var(--font-heading)">75%</text>
</svg>
```

```js
function animateRing(ring, percent, duration = 1200) {
  const circumference = 264;
  const target = circumference * (1 - percent / 100);
  const start = performance.now();

  function update(time) {
    const progress = Math.min((time - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    ring.style.strokeDashoffset = circumference - (circumference - target) * eased;
    if (progress < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}
```

---

## On-Slide-Enter Trigger (JS)

Automatically trigger animations when a slide becomes visible. Add to your main slide JS:

```js
function onSlideEnter(slideEl) {
  // Reset then replay animations
  const animated = slideEl.querySelectorAll('[class*="anim-"]');
  animated.forEach(el => {
    el.style.animation = 'none';
    el.offsetHeight; // force reflow
    el.style.animation = '';
  });

  // Fire counters
  slideEl.querySelectorAll('[data-count]').forEach(el => {
    animateCounter(el, parseInt(el.dataset.count));
  });

  // Fire progress rings
  slideEl.querySelectorAll('[data-ring-percent]').forEach(ring => {
    animateRing(ring.querySelector('.ring-fill'), parseInt(ring.dataset.ringPercent));
  });
}

// Call from your goTo() function:
// function goTo(index) {
//   ...
//   onSlideEnter(slides[current]);
// }
```

---

## Particle Background (Optional)

Lightweight CSS-only particle effect using pseudo-elements:

```css
.slide-particles {
  position: relative;
  overflow: hidden;
}

.slide-particles::before,
.slide-particles::after {
  content: '';
  position: absolute;
  width: 0.5vw;
  height: 0.5vw;
  border-radius: 50%;
  background: var(--accent);
  opacity: 0.3;
  animation: float 6s ease-in-out infinite;
}

.slide-particles::before { top: 20%; left: 10%; animation-delay: 0s; }
.slide-particles::after  { top: 70%; left: 80%; animation-delay: 3s; }

@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); opacity: 0.3; }
  50%       { transform: translateY(-3vh) scale(1.5); opacity: 0.6; }
}
```

---

## Timing Reference

| Effect | Duration | Easing |
|--------|----------|--------|
| Slide transition | 400ms | `cubic-bezier(0.4, 0, 0.2, 1)` (Material standard) |
| Fade in | 300–500ms | `ease` |
| Pop / bounce | 400ms | `cubic-bezier(0.34, 1.56, 0.64, 1)` (spring) |
| Draw / reveal | 500–800ms | `cubic-bezier(0.4, 0, 0.2, 1)` |
| Counter | 1200–1800ms | ease-out cubic (JS) |
| Stagger interval | 80–120ms | — |
