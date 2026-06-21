---
name: CardBranch
description: Premium digital and physical business cards
colors:
  primary: "#6b1f2a"
  primary-hover: "#7c2535"
  gold: "#c9a84c"
  bg-primary: "#f0ebe4"
  bg-secondary: "#faf8f4"
  bg-card: "#faf8f4"
  bg-elevated: "#ffffff"
  text-primary: "#1a1714"
  text-secondary: "#8a7e72"
  text-dim: "#b0a496"
  border: "#d8d0c4"
  border-light: "#e8e2d8"
  avatar-bg: "#f0dde0"
  avatar-border: "#6b1f2a"
  badge-bg: "#f0dde0"
  badge-border: "#d4b0b5"
  success: "#3b6d11"
  success-bg: "#eaf3de"
  success-border: "#b8d89a"
  warning: "#92600a"
  warning-bg: "#fdf3e3"
  warning-border: "#f0d090"
  danger: "#ef4444"
  danger-bg: "rgba(239,68,68,0.08)"
  danger-border: "rgba(239,68,68,0.3)"
typography:
  display:
    fontFamily: "DM Serif Display, serif"
    fontSize: "clamp(2rem, 5vw, 3rem)"
    fontWeight: 400
    lineHeight: 1.2
  headline:
    fontFamily: "DM Serif Display, serif"
    fontSize: "24px"
    fontWeight: 400
    lineHeight: 1.3
  title:
    fontFamily: "Inter, sans-serif"
    fontSize: "16px"
    fontWeight: 600
    lineHeight: 1.4
  body:
    fontFamily: "Inter, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Inter, sans-serif"
    fontSize: "11px"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "0.10em"
rounded:
  sm: "4px"
  md: "6px"
  lg: "8px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
components:
  button-primary:
    backgroundColor: "#6b1f2a"
    textColor: "#faf8f4"
    rounded: "4px"
    padding: "10px 24px"
    fontWeight: 600
    boxShadow: "0 2px 8px rgba(107,31,42,0.35)"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "#6b1f2a"
    border: "1.5px solid #6b1f2a"
    rounded: "4px"
    padding: "10px 24px"
    fontWeight: 500
  button-ghost-light:
    backgroundColor: "transparent"
    textColor: "#faf8f4"
    border: "1px solid rgba(250,248,244,0.3)"
    rounded: "4px"
    padding: "10px 24px"
    fontWeight: 500
  card-container:
    backgroundColor: "#faf8f4"
    rounded: "8px"
    padding: "12px"
    border: "1px solid #d8d0c4"
    boxShadow: "0 3px 12px rgba(107,31,42,0.08), 0 1px 3px rgba(0,0,0,0.04)"
    accentStripe: "4px solid #6b1f2a"
---

# Design System: CardBranch

## 1. Overview

**Creative North Star: "The Executive Wallet"**

CardBranch's visual system is warm, premium, and confident. Linen is the canvas — a warm cream palette that signals quality without coldness. Oxblood is the ink — the single accent colour that runs through every interactive surface, every brand moment, every CTA. The combination reads like a high-end stationer's website: tactile, considered, trustworthy.

The landing page has a dark oxblood nav and a linen body — the nav anchors the brand, the page breathes below it. The dashboard shares the same DNA: linen surfaces, oxblood accents, lifted cards with warm shadows.

The system explicitly rejects: generic SaaS monoculture (indigo-and-white dashboards, stock illustrations), cheap DIY aesthetics (inconsistent spacing, rough edges), cold grey palettes, and dark gamer aesthetics (blue-black, neon, glow effects).

### Key Characteristics
- **Linen foundation.** Page bg #f0ebe4, surface bg #faf8f4. Warm cream, not clinical white, not cool grey.
- **Oxblood accent.** #6b1f2a. Nav bar, card stripes, avatars, badges, buttons, active states, CTA band. The house colour — present everywhere it's earned.
- **Oxblood tint.** #f0dde0. The warm pink-beige used for avatar fills, badge fills, icon fills, and active sidebar backgrounds. Bridges linen and oxblood.
- **Cards are lifted.** Warm oxblood-tinted shadow at rest. Every interactive card surface floats off the page.
- **Bold UI typography.** Card names 600 weight. Labels 700. Confident, not timid.
- **DM Serif Display for headings, Inter for UI.** Editorial serif above, clean sans below.
- **Split register done right.** Landing page breathes with generous hero padding and a product preview in the hero. Dashboard is efficient — tight spacing, sidebar navigation, info-dense layout.

## 2. Colors

### Primary
- **Oxblood** (#6b1f2a): The action colour. Nav bar background, primary buttons, card accent stripes, avatar borders, active sidebar borders. Solid — not diluted.
- **Oxblood hover** (#7c2535): Button hover and pressed states.
- **Oxblood tint** (#f0dde0): Surface tint for avatars, badges, icon backgrounds, active sidebar items, hero pill background.
- **Oxblood tint border** (#d4b0b5): Border on oxblood-tinted surfaces.

### Secondary (product-scoped)
- **Gold** (#c9a84c): Reserved for card view and checkout flow only. Card face previews, order CTAs, public links page. Never used as a system accent.

### Neutral
- **Linen page** (#f0ebe4): Page background. Sits behind all cards and surfaces.
- **Linen surface** (#faf8f4): Card backgrounds, sidebar, top bar. One step lighter than page bg.
- **White** (#ffffff): Input backgrounds, elevated modals.
- **Warm gray** (#8a7e72): Secondary text. Body copy, nav links, non-emphasised content.
- **Muted taupe** (#b0a496): Dim text. Labels, metadata, placeholders, timestamps.
- **Border** (#d8d0c4): All card borders, dividers, row borders.
- **Border light** (#e8e2d8): Internal card dividers.

### Semantic
- **Success:** text #3b6d11, bg #eaf3de, border #b8d89a.
- **Warning:** text #92600a, bg #fdf3e3, border #f0d090.
- **Danger:** text #ef4444, bg rgba(239,68,68,0.08), border rgba(239,68,68,0.3).

## 3. Typography

**Fonts:** DM Serif Display (400) for display and headlines. Inter (400, 500, 600, 700) for all UI text. Load both via Google Fonts in base.html.

**Weight system:** Heavier than a typical linen palette. Card names at 600. Labels at 700. Badges at 700. The oxblood gives the system its warmth — the weight gives it its confidence.

### Hierarchy
- **Display** (DM Serif Display, 400, clamp(2rem, 5vw, 3rem), 1.2): Hero headline on landing page only. Never inside the dashboard. Italic `<em>` spans in oxblood.
- **Headline** (DM Serif Display, 400, 24px, 1.3): Dashboard page titles, section headings on landing.
- **Title / Card name** (Inter, 600, 13–16px, 1.4): Card names, sidebar headings.
- **Body** (Inter, 400, 14px, 1.6): Descriptions, table content. Max 65–75ch line length.
- **Label** (Inter, 700, 9–11px, 1.3): All-caps section labels, table headers, badge text. Letter-spacing 0.08–0.10em.
- **Small** (Inter, 500, 9–10px, 1.4): Roles, metadata, timestamps, card links. Colour: #b0a496.

## 4. Elevation

Cards carry a warm resting shadow. The product sells physical objects — the UI should feel like it has materiality. Shadow is oxblood-tinted, not cold grey.

### Shadow System
- **Card resting:** `0 3px 12px rgba(107,31,42,0.08), 0 1px 3px rgba(0,0,0,0.04)`
- **Order row:** `0 1px 4px rgba(0,0,0,0.04)`
- **Primary button:** `0 2px 8px rgba(107,31,42,0.35)`
- **Modals:** bg #faf8f4, border #d8d0c4, no extra shadow

### Named Rule
**The Warm Lift Rule.** Every interactive card surface has a resting shadow. The shadow is warm and oxblood-tinted. Static panels (sidebar body, flash messages) are flat. Lift signals interactivity.

## 5. Components

### Buttons
- **Primary:** bg #6b1f2a, text #faf8f4, 10px 24px, 4px radius, 600 weight, shadow `0 2px 8px rgba(107,31,42,0.35)`. Hover: #7c2535.
- **Ghost (on linen):** transparent, 1.5px solid #6b1f2a border, #6b1f2a text, 500 weight. Hover: bg #f0dde0.
- **Ghost (on oxblood):** transparent, 1px solid rgba(250,248,244,0.3) border, #faf8f4 text. Used in nav and CTA band.
- **Inverted (CTA band):** bg #faf8f4, text #6b1f2a, 700 weight. The one inverted button in the system.
- **Small variant:** 7px 14px padding, 11px font.

### Cards
- **Corner style:** 8px radius.
- **Background:** #faf8f4.
- **Accent stripe:** 4px solid #6b1f2a at top of every card.
- **Shadow:** `0 3px 12px rgba(107,31,42,0.08), 0 1px 3px rgba(0,0,0,0.04)` — always at rest.
- **Border:** 1px solid #d8d0c4.
- **Padding:** 12px.
- **Avatar:** 28–34px circle, bg #f0dde0, 1.5px solid #6b1f2a border, text #6b1f2a at 700 weight.
- **Card name:** Inter 600, #1a1714.
- **Card role:** Inter 500, 9–10px, #b0a496, letter-spacing 0.04em.
- **Internal divider:** 1px solid #e8e2d8.
- **Card link:** 9px, #8a7e72, Inter 400.
- **Badge:** bg #f0dde0, border 1px solid #d4b0b5, text #6b1f2a, 700 weight, 7–9px, uppercase, letter-spacing 0.05–0.07em, with 3px dot.

### Inputs / Fields
- **Style:** bg #ffffff, 1px solid #d8d0c4, text #1a1714, placeholder #b0a496, 10px 14px padding, 6px radius.
- **Focus:** border #6b1f2a, focus-visible ring 2px oxblood offset.
- **Error:** border #ef4444. **Disabled:** opacity 0.5.

### Navigation — Top Bar
- **Background:** #6b1f2a. The primary brand moment.
- **Logo:** DM Serif Display, #faf8f4.
- **Links:** Inter 12px, rgba(250,248,244,0.55). Active: #faf8f4, 500 weight, 2px solid #faf8f4 bottom border.
- **Ghost button:** transparent, rgba(250,248,244,0.3) border, #faf8f4 text.
- **Solid button (get started):** bg #faf8f4, text #6b1f2a, 700 weight.

### Navigation — Sidebar (Dashboard)
- **Background:** #faf8f4, right border 1px solid #d8d0c4.
- **Logo area:** border-bottom 1px solid #d8d0c4.
- **Section labels:** 8–9px, uppercase, #b0a496, 700 weight, letter-spacing 0.10em.
- **Items:** Inter 11px, #8a7e72. Hover: #1a1714.
- **Active:** bg #f0dde0, text #6b1f2a, left border 2px solid #6b1f2a.

### Status Pills
- **Style:** pill-shaped (20px radius), 3px 10px padding, 8–9px font, 700 weight, uppercase, letter-spacing 0.04em, 1px border.
- **Dispatched:** bg #f0dde0, text #6b1f2a, border #d4b0b5.
- **Pending:** bg #fdf3e3, text #92600a, border #f0d090.
- **Delivered:** bg #eaf3de, text #3b6d11, border #b8d89a.
- **Sent to Print:** same as dispatched.

### Order Rows
- **Style:** bg #faf8f4, border 1px solid #d8d0c4, 6px radius, 8px 10px padding, shadow `0 1px 4px rgba(0,0,0,0.04)`.
- **Icon:** 24–28px square, 4–5px radius, bg #f0dde0, color #6b1f2a.
- **Name:** Inter 600, 10–11px, #1a1714.
- **Date:** Inter 400, 8–9px, #b0a496.

### Stat Cards
- **Style:** bg #faf8f4, border 1px solid #d8d0c4, 7–8px radius, 10–12px padding.
- **Value:** DM Serif Display, 20–26px, #6b1f2a.
- **Label:** Inter 700, 8–9px, uppercase, #b0a496, letter-spacing 0.08em.

### Hero (Landing Page)
- **Page bg:** #f0ebe4.
- **Hero section bg:** #faf8f4, border-bottom 1px solid #d8d0c4.
- **Pill badge:** bg #f0dde0, border 1px solid #d4b0b5, text #6b1f2a, 600 weight.
- **Headline:** DM Serif Display 400, #1a1714. Italic `<em>` in #6b1f2a.
- **Subtext:** Inter 400, #8a7e72.
- **Product preview:** bg #f5f2ed, border #d8d0c4, contains mini card grid in dashboard style.
- **Trust bar:** bg #faf8f4, borders top and bottom #d8d0c4, text #b0a496.

### CTA Band (Landing Page)
- **Background:** #6b1f2a solid.
- **Headline:** DM Serif Display, #faf8f4.
- **Subtext:** rgba(250,248,244,0.6).
- **Button:** bg #faf8f4, text #6b1f2a, 700 weight — the inverted button.

### Flash Messages
- **Error:** text #ef4444, bg rgba(239,68,68,0.08), border rgba(239,68,68,0.3), 6px radius, 12px 20px padding.
- **Success:** text #3b6d11, bg #eaf3de, border #b8d89a.

## 6. Do's and Don'ts

### Do:
- **Do** use #6b1f2a solid for nav bar, primary buttons, card stripes, sidebar active border, CTA band.
- **Do** use #f0dde0 tint for avatar fills, badge fills, icon fills, sidebar active bg, hero pill bg.
- **Do** keep page bg #f0ebe4 and surface bg #faf8f4 — the two-step linen depth is what creates the card lift.
- **Do** give every interactive card a resting shadow. The warm lift rule is non-negotiable.
- **Do** use DM Serif Display for all headings and stat values. Inter for everything else.
- **Do** run Inter at 600 for card names and 700 for labels. Heavy weights signal confidence.
- **Do** include a product preview (mini card grid) inside the hero section — users need to see the product above the fold.
- **Do** close the landing page with an oxblood CTA band.
- **Do** keep the sidebar linen (#faf8f4) — it's part of the product surface, not the nav.

### Don't:
- **Don't** use #6b1f2a as a surface or background fill outside the nav bar and CTA band.
- **Don't** use cold grey shadows — all shadows are warm and oxblood-tinted.
- **Don't** use glassmorphism, gradients, glow effects, or neon.
- **Don't** use pure white (#ffffff) as a page background — it reads clinical. Use #f0ebe4.
- **Don't** use gold (#c9a84c) outside card view and checkout.
- **Don't** use Inter 400 for card names or section labels — too weak.
- **Don't** use uppercase for body copy — labels, headers, badges only.
- **Don't** use side-stripe borders as card accents — the stripe lives at the top.
- **Don't** over-round — cards 8px, buttons 4px, pills only for status tags.
- **Don't** make it look like a weekend project — consistent spacing, intentional alignment, no rough edges.
