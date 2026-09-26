/**
 * Cloudflare Workers entry point.
 *
 * Static files are served straight from the assets directory (see
 * wrangler.jsonc); only /api/* reaches this script. The contact handler is the
 * Pages Function in functions/api/contact.js, reused unchanged, so the Pages
 * and Workers deployments cannot drift apart.
 */

import { onRequest as contact } from '../functions/api/contact.js';

export default {
  async fetch(request, env, ctx) {
    const { pathname } = new URL(request.url);

    if (pathname === '/api/contact') {
      return contact({ request, env, waitUntil: (p) => ctx.waitUntil(p) });
    }

    return env.ASSETS.fetch(request);
  }
};
