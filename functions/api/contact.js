/**
 * POST /api/contact — contact form handler (Cloudflare Pages Function).
 *
 * This directory MUST stay at the repository root, NOT inside site/. Cloudflare
 * reads `functions/` from the repo root and maps the file tree onto URL paths,
 * so functions/api/contact.js serves /api/contact.
 * https://developers.cloudflare.com/pages/functions/routing/
 *
 * Behaviour
 *   - Rejects anything that filled the honeypot, without telling the bot.
 *   - Verifies a Cloudflare Turnstile token when TURNSTILE_SECRET is set.
 *   - Emails the enquiry with Reply-To set to the sender, so replying to the
 *     notification replies to the client.
 *   - Answers JSON to the in-page fetch, or 303s to /thanks for a plain
 *     no-JavaScript form post.
 *
 * Environment (Workers & Pages -> Settings -> Variables and Secrets)
 *   RESEND_API_KEY   required to send   — secret
 *   MAIL_TO          required to send   — where enquiries are delivered
 *   MAIL_FROM        optional           — defaults to Resend's sandbox sender
 *   TURNSTILE_SECRET optional           — secret; skips the check when absent
 *
 * With no mail provider configured the endpoint returns 503 and the form falls
 * back to WhatsApp in the browser, so an enquiry is never silently swallowed.
 * See docs/DEPLOY.md.
 */

const FIELD_LABELS = {
  name: 'Name',
  company: 'Company',
  email: 'Email',
  phone: 'Phone / WhatsApp',
  services: 'Needs',
  message: 'Message',
  enquiry: 'From package',
  page: 'Submitted from'
};

const MAX_LEN = { name: 200, company: 200, email: 320, phone: 60, message: 5000 };

export async function onRequestPost(context) {
  const { request, env } = context;

  let form;
  try {
    form = await request.formData();
  } catch (err) {
    return respond(request, 400, false, 'That submission could not be read.');
  }

  // 1. Honeypot. Accept it so the bot sees success, then drop it.
  if ((form.get('_gotcha') || '').trim()) {
    return respond(request, 200, true, 'Thank you — your enquiry is with us.');
  }

  // 2. Turnstile, when configured.
  if (env.TURNSTILE_SECRET) {
    const token = form.get('cf-turnstile-response') || '';
    const ok = await verifyTurnstile(
      env.TURNSTILE_SECRET,
      token,
      request.headers.get('CF-Connecting-IP')
    );
    if (!ok) {
      return respond(
        request,
        403,
        false,
        'We could not verify that submission. Please try again.'
      );
    }
  }

  // 3. Validate. Mirrors the client-side rules so a direct POST cannot skip them.
  const values = {};
  for (const key of Object.keys(FIELD_LABELS)) {
    if (key === 'services') {
      values.services = form.getAll('services').map(clean).filter(Boolean);
      continue;
    }
    values[key] = clean(form.get(key)).slice(0, MAX_LEN[key] || 500);
  }

  const missing = ['name', 'email', 'message'].filter((k) => !values[k]);
  if (missing.length) {
    return respond(
      request,
      422,
      false,
      'Please fill in your name, email and what the business needs.'
    );
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(values.email)) {
    return respond(request, 422, false, 'That email address does not look right.');
  }

  // 4. Deliver.
  const to = env.MAIL_TO;
  if (!env.RESEND_API_KEY || !to) {
    // Deliberately explicit: the form's catch branch turns this into a
    // WhatsApp hand-off rather than losing the enquiry.
    return respond(
      request,
      503,
      false,
      'The enquiry form is not connected yet.',
      'mail_not_configured'
    );
  }

  try {
    await sendViaResend({
      apiKey: env.RESEND_API_KEY,
      from: env.MAIL_FROM || 'MBC Consultancy <onboarding@resend.dev>',
      to,
      replyTo: values.email,
      subject: subjectFor(values),
      text: bodyFor(values, request)
    });
  } catch (err) {
    return respond(request, 502, false, 'The enquiry could not be sent.');
  }

  return respond(request, 200, true, 'Thank you — your enquiry is with us.');
}

/** Anything other than POST: send people to the form rather than an error page. */
export async function onRequest(context) {
  if (context.request.method === 'POST') return onRequestPost(context);
  if (context.request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: { Allow: 'POST' } });
  }
  return Response.redirect(new URL('/contact', context.request.url).toString(), 303);
}

/* -------------------------------------------------------------------------- */

function clean(value) {
  if (typeof value !== 'string') return '';
  // Strip control characters, including the CR/LF a header-injection attempt
  // would need to smuggle extra headers into the outgoing mail.
  return value.replace(/[\u0000-\u001F\u007F]/g, ' ').trim();
}

async function verifyTurnstile(secret, token, ip) {
  if (!token) return false;
  const body = new FormData();
  body.append('secret', secret);
  body.append('response', token);
  if (ip) body.append('remoteip', ip);
  try {
    const res = await fetch(
      'https://challenges.cloudflare.com/turnstile/v0/siteverify',
      { method: 'POST', body }
    );
    const data = await res.json();
    return data.success === true;
  } catch (err) {
    return false;
  }
}

function subjectFor(values) {
  const who = values.company ? values.name + ' — ' + values.company : values.name;
  const topic = values.services.length ? values.services[0] : 'Enquiry';
  return 'Website enquiry: ' + topic + ' — ' + who;
}

function bodyFor(values, request) {
  const lines = [];
  for (const [key, label] of Object.entries(FIELD_LABELS)) {
    const value = key === 'services' ? values.services.join(', ') : values[key];
    if (!value) continue;
    if (key === 'message') continue; // placed last, on its own
    lines.push(label + ': ' + value);
  }
  lines.push('');
  lines.push('Message');
  lines.push('-------');
  lines.push(values.message);
  lines.push('');
  lines.push('---');
  const country = request.headers.get('CF-IPCountry');
  lines.push(
    'Sent from the MBC Consultancy website' + (country ? ' (' + country + ')' : '')
  );
  lines.push('Reply directly to this email to answer ' + values.name + '.');
  return lines.join('\n');
}

async function sendViaResend({ apiKey, from, to, replyTo, subject, text }) {
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: 'Bearer ' + apiKey,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      from,
      to: [to],
      reply_to: replyTo,
      subject,
      text
    })
  });
  if (!res.ok) {
    throw new Error('Resend responded ' + res.status + ': ' + (await res.text()));
  }
  return res.json();
}

/**
 * One reply shape for two callers: the enhanced form reads JSON, a plain HTML
 * form post follows a redirect.
 */
function respond(request, status, ok, message, code) {
  const wantsJson = (request.headers.get('Accept') || '').includes('application/json');
  if (wantsJson) {
    return new Response(JSON.stringify({ ok, message, code }), {
      status,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });
  }
  const target = ok ? '/thanks' : '/contact?error=1#enquiry';
  return Response.redirect(new URL(target, request.url).toString(), 303);
}
