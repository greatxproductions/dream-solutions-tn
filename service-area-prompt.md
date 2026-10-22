Continue building the existing Astro site in this directory — a website for "Dream Solutions Tennessee", a radon mitigation company. The core site (7 pages, components, design system) is already built and committed. Do NOT modify or rebuild existing pages/components/design.

Your task: add the service-area pages.

FIRST read these files to match conventions exactly:
- service-area-content.md (content brief: city list, accurate facts, per-page structure)
- src/layouts/Layout.astro, src/components/SeoHead.astro, src/styles/global.css
- src/pages/index.astro (example page structure)

Then create:
1. src/pages/service-areas/index.astro — intro + list of all 8 cities linking to their pages.
2. src/pages/service-areas/[slug].astro — a dynamic route using getStaticPaths that renders the 8 city pages (slugs: nashville, gallatin, hendersonville, franklin, murfreesboro, brentwood, lebanon, mt-juliet). Use the city-specific copy and the verified EPA facts from service-area-content.md. Do NOT invent radon statistics, testimonials, or license numbers.

Also:
- Update public/sitemap.xml to include the service-area pages.
- Each city page: unique <title> and meta description, LocalBusiness schema with areaServed set to the city, and a CTA linking to /contact.

Verify `npm run build` exits 0. Report the files you created and confirm the build passed.
