import type { APIRoute } from 'astro';
// Static preview artifact only. POST requires a deployed backend (e.g. a Pages Function).
export const prerender = true;
const response = () => new Response(JSON.stringify({ ok: true }), {
  headers: { 'Content-Type': 'application/json' },
});
export const GET: APIRoute = response;
export const POST: APIRoute = response;
