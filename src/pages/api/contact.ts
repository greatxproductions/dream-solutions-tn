import type { APIRoute } from 'astro';

export const prerender = false;

function escapeHtml(s: string) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });

export const GET: APIRoute = () => json({ ok: true });

export const POST: APIRoute = async ({ request }) => {
  let data: Record<string, string> = {};
  const contentType = request.headers.get('content-type') || '';
  try {
    if (contentType.includes('application/json')) {
      data = (await request.json()) as Record<string, string>;
    } else {
      const fd = await request.formData();
      for (const [k, v] of fd.entries()) data[k] = String(v);
    }
  } catch {
    return json({ ok: false, error: 'Invalid request.' }, 400);
  }

  const name = (data.name || '').trim();
  const email = (data.email || '').trim();
  const phone = (data.phone || '').trim();
  const service = (data.service || 'Other').trim();
  const message = (data.message || '').trim();

  if (!name || !email) {
    return json({ ok: false, error: 'Name and email are required.' }, 400);
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ ok: false, error: 'Please enter a valid email address.' }, 400);
  }

  // Env vars live in the Workers runtime — locals.runtime.env was removed in Astro v6.
  const { env } = await import('cloudflare:workers');
  const e = env as any;
  const RESEND_API_KEY: string = e.RESEND_API_KEY || '';
  const FROM: string = e.LEAD_FROM_EMAIL || 'Dream Solutions TN <leads@dreamsolutionstn.com>';
  const TO: string[] = (e.LEAD_TO_EMAILS || '')
    .split(',')
    .map((s: string) => s.trim())
    .filter(Boolean);

  if (!RESEND_API_KEY || TO.length === 0) {
    return json({ ok: false, error: 'Email service is not configured yet.' }, 500);
  }

  const html =
    `<h2 style="font-family:sans-serif">New lead from Dream Solutions TN</h2>` +
    `<p><strong>Name:</strong> ${escapeHtml(name)}</p>` +
    `<p><strong>Phone:</strong> ${escapeHtml(phone || '—')}</p>` +
    `<p><strong>Email:</strong> ${escapeHtml(email)}</p>` +
    `<p><strong>Service:</strong> ${escapeHtml(service)}</p>` +
    `<p><strong>Message:</strong></p><p>${escapeHtml(message || '—')}</p>`;

  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: FROM,
        to: TO,
        reply_to: email,
        subject: `New lead: ${name} — ${service}`,
        html,
      }),
    });
    const body = await res.json().catch(() => ({}));
    if (!res.ok) {
      return json({ ok: false, error: (body as any).message || 'Failed to send.' }, 502);
    }
    return json({ ok: true, id: (body as any).id });
  } catch {
    return json({ ok: false, error: 'Failed to send your message. Please call or email us directly.' }, 500);
  }
};
