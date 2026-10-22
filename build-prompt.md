Build a production-quality static website for "Dream Solutions Tennessee", a radon mitigation company based in Nashville, TN. Work entirely inside this repository (the current worktree).

CONTEXT (all true, do not invent beyond this):
- Company: Dream Solutions Tennessee — radon mitigation services: radon testing, radon mitigation system installation, crawl space encapsulation / vapor barrier.
- Founders: Khary Cammock and Patrick Donnelly.
- Service area: Nashville, TN and surrounding Middle Tennessee territories.
- Phone: use the placeholder "(615) 555-0123" everywhere a phone appears. Do NOT invent any other phone number.
- No logo yet: render the brand as a clean text wordmark "Dream Solutions Tennessee" (optionally with a simple inline SVG house/shield glyph — keep it tasteful and CSS-only).
- No physical address shown (service-area business). Do NOT invent an address.
- No fake testimonials, no fake license numbers, no pricing.

TECH:
- Astro static site. Scaffold with `npm create astro@latest . -- --template minimal --no-install --no-git` (adapt flags as needed so it lands in the current directory), then `npm install`.
- Styling: Tailwind CSS via `npx astro add tailwind --yes` (or clean hand-written CSS with variables if Tailwind setup fails — prefer Tailwind).
- Must build cleanly: `npm run build` exits 0 and emits to `dist/`. It will be deployed to Cloudflare Pages (no adapter needed beyond static output).
- Responsive, mobile-first, accessible, fast.

DESIGN INSPIRATION (from giordanobetti.com — an editorial/cinematic aesthetic; adapt it, do not copy content):
- Palette: dark charcoal/off-black background (#121212–#141414), off-white primary text (#EFEFEF–#F5F5F5), muted gray secondary text (#7A7A7A–#888888), thin white accent hairlines. No bright gradients, no heavy UI chrome.
- Typography: pair a high-contrast editorial serif for display headlines (Playfair Display, Roslindale, Cormorant, or a Didone-style serif) with a clean sans-serif for nav/body/labels (Inter, Helvetica Neue, or system sans). Headlines can be large, refined, with modest letter-spacing; body text tight line-height.
- Layout: editorial, asymmetric grid, vast negative space. No cards/boxes/borders — structure via proximity, alignment, and hairline rules. Pinned header and footer with an open center stage.
- Mood: understated premium, gallery-like, confident. For a home-services company this should read as clean and trustworthy, not gothic — keep it crisp and professional.
- The radon content (health/safety/trust) must stay front and center; the dark editorial style should elevate it, not obscure it.

PAGES (create in src/pages/):
1. `/` index — hero (headline + subhead + primary CTA "Get a Free Estimate" linking to /contact), what radon is / why it matters (EPA action level 4.0 pCi/L), services overview (3 cards linking to each service page), service-area summary, trust/credibility strip, secondary CTA.
2. `/radon-testing` — what radon is, health risks, why testing matters, how the testing process works, EPA 4.0 pCi/L action level, CTA.
3. `/radon-mitigation` — what a mitigation system is, how it works, the process, why professional installation matters, CTA.
4. `/crawl-space-encapsulation` — vapor barrier / encapsulation service, benefits, CTA.
5. `/about` — the two founders (Khary Cammock, Patrick Donnelly), company mission, why choose us.
6. `/contact` — lead form with fields: Name, Phone, Email, Service needed (select: Radon Testing / Radon Mitigation / Crawl Space Encapsulation / Other), Message. Form method POST action `/api/contact`. Also show phone + service area. The `/api/contact` endpoint does not need a real implementation yet — create a stub `src/pages/api/contact.ts` (or .js) that returns a JSON `{ok:true}` (I will wire the real email backend separately).
7. `/404` — clean 404.

COMPONENTS (src/components/): Header (nav + wordmark + CTA), Footer (wordmark, quick links, service area, phone), Hero, ServiceCard, ContactForm, SeoHead (title/description/OG). Use a shared Layout.

SEO / technical:
- Every page: unique <title> and meta description, Open Graph tags, and appropriate heading structure.
- Home page: LocalBusiness schema (JSON-LD) with name, service area, phone placeholder, and service type.
- `public/robots.txt` and `public/sitemap.xml` (list the pages; service-area child pages can be added later).
- No external CDN dependencies that could break offline — bundle fonts locally or use system font stack.

CONSTRAINTS:
- Static only. No server, no database, no external services.
- Do NOT add pricing, fake testimonials, fake credentials, a real address, or any phone other than the placeholder.
- Keep everything self-contained and reproducible.

ACCEPTANCE (verify before reporting):
- `npm install` succeeds and `npm run build` exits 0.
- All listed pages render and cross-link correctly.
- Site is responsive and visually professional.
- The contact form posts to `/api/contact` and the stub endpoint exists.

REPORT BACK (in your final message):
- The list of files you created.
- Confirm `npm run build` passed (quote the exit status / final lines).
- Any decisions you made (design system, fonts) and anything I should know for the next step.
