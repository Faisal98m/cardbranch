# CardBranch Frontend Audit

**Date**: 2026-05-23
**Tool**: impeccable audit
**Scored**: 5 dimensions, 0-4 each, max 20

---

## Audit Health Score: 10/20 (Acceptable)

| # | Dimension | Score | Key Finding |
|---|-----------|-------|-------------|
| 1 | Accessibility | **2** | No main landmark, no focus indicators, hover effects keyboard-inaccessible |
| 2 | Performance | **3** | Google Fonts render-blocking, no CSS caching, unoptimized uploads |
| 3 | Theming | **1** | Zero design tokens, hard-coded colors throughout, single theme only |
| 4 | Responsive Design | **2** | No media queries, nav breaks on mobile, admin cramped at narrow widths |
| 5 | Anti-Patterns | **2** | Gradient text ban violation, dark+gold AI palette tells |
| **Total** | | **10/20** | **Acceptable (significant work needed)** |

**Rating bands**: 18-20 Excellent (minor polish), 14-17 Good (address weak dimensions), 10-13 Acceptable (significant work needed), 6-9 Poor (major overhaul), 0-5 Critical (fundamental issues)

---

## Anti-Patterns Verdict

**FAIL** - Gradient text (`background-clip: text` with `linear-gradient`) on both the landing page headline and the public links page brand name violates the impeccable absolute ban. The dark + gold + gradient text combination reads as an AI-generated template.

---

## Detailed Findings by Severity

### P1: Gradient text on landing page and links page

- **Location**: `templates/public/index.html:22`, `templates/public/links.html:16`
- **Category**: Anti-Pattern
- **Impact**: Violates the impeccable absolute ban on `background-clip: text` with gradients. Makes the brand look generic.
- **Recommendation**: Use a single solid gold (`#c9a96e`) for emphasis. Use weight/size contrast instead of gradient.
- **Suggested command**: `colorize`

### P1: No keyboard-accessible hover states

- **Location**: `templates/dashboard/index.html` (cards), `templates/public/links.html` (link buttons)
- **Category**: Accessibility
- **Impact**: `onmouseover`/`onmouseout` only trigger on mouse hover. Keyboard users (Tab navigation) see no visual feedback. WCAG 2.1.1 violation.
- **Recommendation**: Replace inline event handlers with CSS `:hover` and `:focus-visible` pseudo-classes.
- **Suggested command**: `harden`

### P1: No visible focus indicators anywhere

- **Location**: `templates/layouts/base.html` (base styles)
- **Category**: Accessibility
- **Impact**: Keyboard-only users cannot see which element has focus. WCAG 2.4.7 violation.
- **Recommendation**: Add `:focus-visible { outline: 2px solid #c9a96e; outline-offset: 2px; }` to base styles.
- **Suggested command**: `harden`

### P1: No `<main>` landmark

- **Location**: `templates/layouts/base.html:18`
- **Category**: Accessibility
- **Impact**: Screen readers cannot skip directly to page content. WCAG 2.4.1 violation.
- **Recommendation**: Wrap `{% block content %}` in `<main>` element.
- **Suggested command**: `harden`

### P2: Zero design tokens, hard-coded colors

- **Location**: Every template file
- **Category**: Theming
- **Impact**: Over 50 instances of raw hex values (`#0a0a0a`, `#111`, `#c9a96e`, `#222`, `#888`, `#1a1a1a`, `#333`, `#666`, `#131313`, `#fff`) hard-coded across 16 templates. Changing the palette requires editing every file.
- **Recommendation**: Extract to CSS custom properties in base.html: `--bg-primary: #0a0a0a`, `--bg-card: #111`, `--accent-gold: #c9a96e`, `--text-primary: #fff`, `--text-muted: #888`, `--border: #222`. Reference these in all templates.
- **Suggested command**: `extract`

### P2: Nav bar not responsive

- **Location**: `templates/layouts/dashboard.html`, `templates/layouts/admin.html`
- **Category**: Responsive Design
- **Impact**: At viewports <500px, the horizontal nav links overflow/break layout.
- **Recommendation**: Add a media query collapsing nav links behind a toggle, or wrap them with `flex-wrap: wrap` and reduce gap.
- **Suggested command**: `adapt`

### P2: Admin order action buttons have undersized touch targets

- **Location**: `templates/admin/orders.html:55`
- **Category**: Responsive Design
- **Impact**: The "Update" button has `padding: 4px 10px` giving ~28px height, well below the 44px minimum touch target. WCAG 2.5.5 violation.
- **Recommendation**: Increase paddings to meet 44x44px minimum for all interactive elements.
- **Suggested command**: `adapt`

### P2: Google Fonts render-blocking

- **Location**: `templates/layouts/base.html:6-8`
- **Category**: Performance
- **Impact**: The Google Fonts stylesheet blocks rendering. Users see a blank page until the font loads.
- **Recommendation**: Add `display=swap` to the Google Fonts URL for non-blocking font loading.
- **Suggested command**: `optimize`

### P2: `target="_blank"` without `rel="noopener"` in card_view

- **Location**: `templates/dashboard/card_view.html:32`
- **Category**: Accessibility / Performance
- **Impact**: Security vulnerability (tab-napping) and performance issue. Links page (`links.html`) correctly includes `rel="noopener"` but card_view doesn't.
- **Recommendation**: Add `rel="noopener noreferrer"` to all `target="_blank"` links.
- **Suggested command**: `harden`

### P3: Logo uploads not optimized

- **Location**: `app/services/generator.py:save_logo`
- **Category**: Performance
- **Impact**: Users can upload large images served at full resolution. No resizing or format conversion.
- **Recommendation**: Resize uploaded logos to a max dimension (e.g., 400px) and convert to WebP.
- **Suggested command**: `optimize`

### P3: Inline CSS repeated in every page load

- **Location**: All templates
- **Category**: Performance
- **Impact**: Styles are in `<style>` blocks inside base.html, loaded with every page. No browser caching between pages.
- **Recommendation**: Extract to an external `style.css` file with cache headers.
- **Suggested command**: `polish`

---

## Positive Findings

- **Form labels**: Every `<label>` element is properly associated with its input via WTForms - solid a11y baseline.
- **Semantic heading hierarchy**: Pages progress h1 -> h2 -> h3 without skipping levels.
- **Server-rendered architecture**: Fast TTFB, no client-side JS bloat. Performance baseline is solid.
- **Logo alt text**: Links page uses `alt="{{ client.brand_name }}"` - good descriptive alt text.
- **`overflow-x: auto` on tables**: Admin tables are wrapped in scroll containers, preventing layout breakage on narrow screens.
- **Consistent color palette**: Despite being hard-coded, the dark + gold scheme is applied consistently across all pages.

---

## Recommended Actions

1. **[P1] `impeccable harden`**: Add `<main>` landmark, `:focus-visible` styles, `rel="noopener"`, keyboard-accessible hover states
2. **[P1] `impeccable colorize`**: Replace gradient text with solid gold on landing page and links page
3. **[P2] `impeccable extract`**: Extract hard-coded colors into CSS custom properties in base.html
4. **[P2] `impeccable adapt`**: Fix nav responsiveness, increase admin action touch targets
5. **[P2] `impeccable optimize`**: Add `display=swap` to Google Fonts URL
6. **[P3] `impeccable polish`**: Extract inline CSS to external stylesheet

---

*Generated by impeccable audit. Re-run after fixes to see your score improve.*
