You are upgrading the EXISTING Astro site in this directory (dreamsolutionstn.com, "Dream Solutions Tennessee", a radon mitigation company). The site is already live and working. Your job is a visual/interactive upgrade — make it "popping, futuristic, and interactive" and premium/"the best" in its category. Do NOT break anything that works.

## Current state (read these first)
- Styling is 100% in `src/styles/global.css` (currently minified — you may reformat it into organized, readable sections, but keep every existing rule's behavior unless you are intentionally changing it).
- Components: `src/components/{Header,Hero,ServiceCard,CallToAction,ContactForm,Footer,SeoHead}.astro`, `src/layouts/Layout.astro`.
- Pages: index, about, contact, radon-testing, radon-mitigation, crawl-space-encapsulation, service-areas/index, service-areas/[slug], 404.
- Built with Astro + Tailwind 4 (@tailwindcss/vite). Deploys to Cloudflare Workers (do NOT change astro.config.mjs, package.json, or the /api/contact handler).
- The lead form posts to `/api/contact` (already wired to Resend). Keep the form's field names exactly: name, email, phone, service, message.

## Design direction: "aqua-futuristic"
Keep the existing ocean-beach identity but push it toward a glowing, modern, glassy, motion-rich aesthetic. Base palette (DO NOT change these core values — you may add brighter/vivid variants for glows and gradients):
- Sand background #F7F2E8, deep ocean text #0F3D4A, muted #54787F, hairlines #0E5A6426
- Turquoise #0E7C86, golden #C9932B, coral #E56B4F
- Serif display (Didot/Bodoni), sans body (Inter/Helvetica)
The vibe: sunlight on Caribbean water, glass, light particles, gentle motion — not neon cyberpunk. Premium and calm, but alive.

## Features to ADD (all must work, all must respect `prefers-reduced-motion: reduce` by disabling motion)
1. **Animated aurora/gradient background** — soft, slowly drifting gradient blobs (ocean blue / turquoise / warm golden) layered behind content, very subtle so text stays readable. Implement in the layout so it's site-wide.
2. **Scroll-reveal animations** — elements fade/slide up (and can stagger) as they enter the viewport. Use a tiny IntersectionObserver (vanilla JS, no library). Add a `.reveal` utility and apply it to sections, cards, headings.
3. **Hover interactions** — service cards and buttons lift and gain a soft glow / border glow on hover; links animate an underline. Smooth 150–250ms transitions.
4. **Glassmorphism** — service cards and the header become frosted glass (semi-transparent white/teal with `backdrop-filter: blur`), with a subtle glowing border. Must still be readable on the sand background.
5. **Animated headline/gradient text** — key words in hero headlines get an animated gradient (turquoise → golden → coral) or a shimmer sweep.
6. **Animated counters** — the stats on the about page (and any numeric stat) count up when scrolled into view.
7. **Marquee ticker** — the "trust strip" / service tagline becomes a smooth auto-scrolling marquee (pauses or stops for reduced motion).
8. **Cursor glow / spotlight** — a soft radial glow follows the pointer on the page (pointer-events: none, disabled on touch/reduced-motion).
9. **Floating decorative elements** — subtle floating shapes (bubbles/light particles) in the hero, gently drifting (CSS keyframes).
10. **Hero parallax or drift** — the house illustration subtly drifts or the hero copy parallaxes on scroll (keep it light; disable on reduced motion).
11. **Button micro-interactions** — primary buttons get a glowing gradient fill, hover sweep, and press-down scale. Keep the existing "Get a Free Estimate" text and ↗ arrow.
12. **Tech grid / noise overlay** — a faint background grid or fine grain that adds depth without hurting readability.

## Hard constraints
- Preserve ALL existing content, copy, page structure, links, and the "Founded by Khary Cammock & Patrick Donnelly" founder info.
- Keep the SEO meta (SeoHead), sitemap, LocalBusiness schema, service-area pages, and the contact form + Resend backend exactly functional.
- Keep the house-art SVG illustration and its current colors (driftwood #8A6A4E house, turquoise circle, coral dot, deep-ocean pipe/arrows).
- Performance: no heavy JS frameworks. Vanilla JS + CSS only. Keep the bundle lean (target well under ~100KB added JS, ideally a few KB).
- Accessibility: preserve focus-visible states, semantic HTML, aria labels, alt text, and reduced-motion support.
- Do NOT touch `astro.config.mjs`, `package.json`, `deploy.sh`, or `src/pages/api/contact.ts`.
- Make sure `npm run build` exits 0.

## Deliverable
Make the edits, run `npm run build` to confirm it passes, and report exactly what you changed (files + features) and confirm the build result.
