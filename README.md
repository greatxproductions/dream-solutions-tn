# Dream Solutions Tennessee

Static Astro website with Tailwind CSS v4, ready for Cloudflare Pages.

## Run

Use Node.js 22.23.4 or newer (see package.json).

```sh
npm install
npm run dev -- --background
npm run build
npm run preview
```

Cloudflare Pages build command: `npm run build`. Output directory: `dist`.
No adapter, environment variables, database, or runtime services are needed for the website.
Stop the development server with `npm run astro -- dev stop`.

## Design

Charcoal background, warm off-white text, muted neutral accents, editorial spacing,
and fine rules. System Didot/Bodoni/Times display serif and Helvetica Neue/Arial
sans-serif require no font downloads. Original inline SVG architectural illustration;
no external images or client-side JavaScript dependencies. Keyboard focus, skip link,
semantic headings, reduced-motion support, and native form validation included.

## Contact backend handoff

The form uses `method="POST" action="/api/contact"`. Fields: `name`, `phone`,
`email`, `service`, `message`. The source stub at `src/pages/api/contact.ts` exports
POST returning `{ "ok": true }`, verified in Astro development mode.

**Static hosting cannot execute POST handlers.** The build prerenders GET to
`dist/api/contact` for a static JSON artifact; it does not provide a working
production form handler. Visitors see an explicit notice that online requests are
not connected. When wiring email, implement a Cloudflare Pages Function for
`/api/contact` (or configure another backend), remove the static stub to avoid route
conflicts, validate and limit input on the backend, and update the form notice and
submission response. No submissions are currently saved or emailed.

## SEO and deployment

Canonical URLs, robots.txt, sitemap.xml, and schema use https://dreamsolutionstn.com,
as identified in the existing project plan. Update all of them if the final domain
changes. The sitemap lists public content pages and intentionally excludes the 404
and API stub. Open Graph metadata uses a local SVG; some social networks require a
PNG/JPEG preview, so convert the SVG before configuring those platforms.

All visible phone numbers are the required placeholder `(615) 555-0123`.
No physical address, prices, testimonials, or credentials are asserted.
Health guidance links directly to EPA and CDC sources.

## Verification completed

- npm install: exit 0, zero reported vulnerabilities at installation.
- npm run build: exit 0; seven static pages plus API JSON artifact.
- Chromium checks: all seven pages at 390, 768, and 1440px; no horizontal overflow,
  one H1 and title/description/Open Graph tags on each page.
- Desktop and full-page mobile home screenshots visually reviewed.
- Form method, action, all five fields, and development POST response verified.
- Generated internal links checked against built files.

## Created files

- `src/pages/index.astro`
- `src/pages/radon-testing.astro`
- `src/pages/radon-mitigation.astro`
- `src/pages/crawl-space-encapsulation.astro`
- `src/pages/about.astro`
- `src/pages/contact.astro`
- `src/pages/404.astro`
- `src/pages/api/contact.ts`
- `src/components/Header.astro`
- `src/components/Footer.astro`
- `src/components/Hero.astro`
- `src/components/ServiceCard.astro`
- `src/components/ContactForm.astro`
- `src/components/SeoHead.astro`
- `src/components/CallToAction.astro`
- `src/layouts/Layout.astro`
- `src/styles/global.css`
- `public/favicon.svg`
- `public/og-image.svg`
- `public/robots.txt`
- `public/sitemap.xml`
- `astro.config.mjs`, `package.json`, `package-lock.json`, `tsconfig.json`
- `.gitignore`, `.vscode/extensions.json`, `.vscode/launch.json`, `AGENTS.md`
- `README.md`

The existing build-prompt.md and task_plan.md were preserved.
