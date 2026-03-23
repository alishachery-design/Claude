# Style Presets

Pre-defined visual themes for frontend slide presentations. Each preset defines CSS custom properties that override the defaults in `viewport-base.css`.

---

## dark-minimal

Clean, dark background with high-contrast text. Great for tech talks.

```css
:root {
  --bg-primary: #0d0d0d;
  --bg-secondary: #1a1a1a;
  --text-primary: #f0f0f0;
  --text-secondary: #a0a0a0;
  --accent: #00e5ff;
  --accent-secondary: #7c4dff;
  --font-heading: 'Inter', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --slide-padding: 6vw;
  --heading-size: 5vw;
  --body-size: 2.2vw;
  --line-height: 1.6;
  --border-radius: 0.5vw;
}
```

---

## light-clean

Bright, minimal white theme. Ideal for business and academic presentations.

```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --text-primary: #1a1a1a;
  --text-secondary: #555555;
  --accent: #0070f3;
  --accent-secondary: #ff4081;
  --font-heading: 'Playfair Display', Georgia, serif;
  --font-body: 'Source Sans Pro', system-ui, sans-serif;
  --font-mono: 'Source Code Pro', monospace;
  --slide-padding: 8vw;
  --heading-size: 4.5vw;
  --body-size: 2vw;
  --line-height: 1.7;
  --border-radius: 0.3vw;
}
```

---

## gradient-bold

Vivid gradient backgrounds with bold typography. Great for marketing and creative pitches.

```css
:root {
  --bg-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --bg-secondary: rgba(255, 255, 255, 0.1);
  --text-primary: #ffffff;
  --text-secondary: rgba(255, 255, 255, 0.75);
  --accent: #ffd700;
  --accent-secondary: #ff6b6b;
  --font-heading: 'Montserrat', system-ui, sans-serif;
  --font-body: 'Open Sans', system-ui, sans-serif;
  --font-mono: 'Courier New', monospace;
  --slide-padding: 7vw;
  --heading-size: 5.5vw;
  --body-size: 2.3vw;
  --line-height: 1.5;
  --border-radius: 1vw;
}
```

---

## terminal

Retro terminal aesthetic. Perfect for developer talks and hacker culture presentations.

```css
:root {
  --bg-primary: #0c0c0c;
  --bg-secondary: #1c1c1c;
  --text-primary: #00ff41;
  --text-secondary: #008f11;
  --accent: #00ff41;
  --accent-secondary: #ffff00;
  --font-heading: 'VT323', 'Courier New', monospace;
  --font-body: 'Share Tech Mono', 'Courier New', monospace;
  --font-mono: 'Share Tech Mono', 'Courier New', monospace;
  --slide-padding: 5vw;
  --heading-size: 5vw;
  --body-size: 2.5vw;
  --line-height: 1.8;
  --border-radius: 0;
}
```

---

## corporate-blue

Professional blue theme for enterprise and corporate settings.

```css
:root {
  --bg-primary: #003366;
  --bg-secondary: #004080;
  --text-primary: #ffffff;
  --text-secondary: #b3ccee;
  --accent: #ffa500;
  --accent-secondary: #66aaff;
  --font-heading: 'Roboto', system-ui, sans-serif;
  --font-body: 'Roboto', system-ui, sans-serif;
  --font-mono: 'Roboto Mono', monospace;
  --slide-padding: 7vw;
  --heading-size: 4.5vw;
  --body-size: 2.1vw;
  --line-height: 1.6;
  --border-radius: 0.4vw;
}
```

---

## nature-calm

Earthy greens and warm tones. Ideal for environmental, wellness, and lifestyle topics.

```css
:root {
  --bg-primary: #1a2e1a;
  --bg-secondary: #2d4a2d;
  --text-primary: #e8f5e8;
  --text-secondary: #a8c8a8;
  --accent: #7bc67b;
  --accent-secondary: #d4a856;
  --font-heading: 'Lora', Georgia, serif;
  --font-body: 'Nunito', system-ui, sans-serif;
  --font-mono: 'Inconsolata', monospace;
  --slide-padding: 8vw;
  --heading-size: 4.5vw;
  --body-size: 2.2vw;
  --line-height: 1.75;
  --border-radius: 0.8vw;
}
```

---

## Applying a Preset

Add the preset variables to the top of your slide's `<style>` block or in a linked CSS file, before importing `viewport-base.css` defaults:

```html
<style>
  /* 1. Choose a preset */
  :root {
    --bg-primary: #0d0d0d;
    /* ... rest of preset ... */
  }

  /* 2. Import base styles */
  @import url('viewport-base.css');

  /* 3. Add custom overrides */
  .my-special-slide {
    background: var(--accent);
  }
</style>
```

## Custom Fonts

Presets reference Google Fonts. Add the relevant `<link>` tags to your HTML `<head>`:

```html
<!-- Example for dark-minimal (Inter) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
```
