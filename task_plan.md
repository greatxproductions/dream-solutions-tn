# Dream Solutions Tennessee — Website Build Plan

## Goal
Build and deploy a lead-generating website for Dream Solutions Tennessee (Radon Mitigation) at dreamsolutionstn.com, hosted on Cloudflare Pages, with a lead form that emails both founders (KCammock@ and PDonnelly@ once Workspace is live).

## Current State (verified live)
- Domain `dreamsolutionstn.com` live on Cloudflare (NS randall/veda).
- Cloudflare API token stored in `~/.hermes/.env` (DNS-edit scope, zone `76095eded3f928517fb2540d873d935f`).
- Email auth done: SPF + DKIM + DMARC + MX (5 ASPMX records) + verification TXT/CNAME.
- Google Workspace verification pending (Google-side lag on a same-day domain).
- Orca + Codex available for the build (orca-dispatch → worktree → Codex).
- Resend: available for transactional email; API key NOT yet in hand.

## Tech Stack (recommended)
- Static site: **Astro** (fast, SEO-first, component-based, deploys cleanly to Cloudflare Pages).
- Hosting: **Cloudflare Pages** (free tier, already on Cloudflare, domain DNS points there).
- Styling: Tailwind CSS.
- Lead form: **Cloudflare Pages Function** (serverless) → **Resend** → email to both founders. No third-party form service, no server to run.

## Site Map
1. Home — hero, trust signals, services overview, service area, CTA.
2. Radon Testing
3. Radon Mitigation
4. Crawl Space Encapsulation / Vapor Barrier
5. About — founders (Khary Cammock + Patrick Donnelly)
6. Contact — lead form + phone + service area
7. Service-area pages (local SEO): Nashville + Middle TN surrounding territories (Gallatin, Hendersonville, Franklin, Murfreesboro, Brentwood, Lebanon, Mt. Juliet; Sumner/Davidson/Williamson counties).

## SEO / Local
- Google Business Profile (user action; agent guides).
- LocalBusiness + Service schema markup.
- Sitemap.xml, robots.txt, meta titles/descriptions.
- Service-area pages targeting Tennessee cities/counties.

## Phases
1. Repo + scaffolding — git init, Astro project, Orca worktree.
2. Pages + content — Codex builds all pages (copy needs founder approval).
3. Lead form backend — Cloudflare Pages Function + Resend wiring.
4. SEO — schema, sitemap, meta, service-area pages.
5. Deploy — Cloudflare Pages + DNS A/CNAME records.
6. Verify — end-to-end form test, Lighthouse, mobile check, live URL.

## You vs Me
**You (blockers to resolve):**
- Business phone number
- Service area (cities/counties)
- Physical address or service-area-only (for Google Business Profile)
- Resend API key (or authorize me to source one)
- Approve page copy / tone
- Any logo/branding (else text-based placeholder)

**Me / Orca:**
- All code, deploy, DNS, form backend, SEO scaffolding.

## Progress Log
- [x] Domain purchased + on Cloudflare (NS randall/veda).
- [x] Email DNS: MX (5 ASPMX), SPF, DKIM, DMARC, verification TXT + CNAME — all live and verified.
- [x] Repo init + initial commit.
- [x] Build spec written (build-prompt.md) with giordanobetti.com editorial design language.
- [~] Core site build — Codex running (background).
- [~] Service-area content brief written (service-area-content.md) — ready for next Codex pass.
- [~] GBP listing draft written (gbp-listing.md).
- [ ] Service-area pages (8 cities) — next Codex pass.
- [ ] Lead form backend — Resend wiring.
- [ ] Deploy to Cloudflare Pages + DNS A/CNAME.
- [ ] Google Workspace verification (waiting on Google lag) + create 2 users.
- [ ] Google Business Profile (user action; content prepared).

## Blockers (user-only)
- Google Workspace: click Verify (laptop), create KCammock@ + PDonnelly@ users, billing.
- Google Business Profile: submit (content ready in gbp-listing.md).
- Resend: verify dreamsolutionstn.com (needs full-access key or Resend dashboard login).
- Real phone number (dummy placeholder in use).

