#!/bin/bash
# Build + deploy Dream Solutions TN to Cloudflare Workers.
# Usage: CLOUDFLARE_API_TOKEN=... CLOUDFLARE_ACCOUNT_ID=... ./deploy.sh
set -euo pipefail
cd "$(dirname "$0")"

# Source env; wrangler needs CLOUDFLARE_API_TOKEN to be the Pages/Workers token
# (CLOUDFLARE_PAGES_TOKEN), NOT the DNS-edit token (CLOUDFLARE_API_TOKEN).
if [ -f "$HOME/.hermes/.env" ]; then
  set -a; . "$HOME/.hermes/.env"; set +a
fi
export CLOUDFLARE_API_TOKEN="${CLOUDFLARE_PAGES_TOKEN:-$CLOUDFLARE_API_TOKEN}"

echo "=== build ==="
npm run build

echo "=== patch generated wrangler.json (routes + vars) ==="
python3 - <<'PY'
import json, pathlib, os
p = pathlib.Path('dist/server/wrangler.json')
cfg = json.loads(p.read_text())
cfg['routes'] = [
    {"pattern": "dreamsolutionstn.com/*", "zone_name": "dreamsolutionstn.com"},
    {"pattern": "www.dreamsolutionstn.com/*", "zone_name": "dreamsolutionstn.com"},
]
cfg['vars'] = {
    # Update LEAD_TO_EMAILS once Google Workspace users exist.
    "LEAD_FROM_EMAIL": os.environ.get("LEAD_FROM_EMAIL", "Dream Solutions TN <leads@dreamsolutionstn.com>"),
    "LEAD_TO_EMAILS": os.environ.get("LEAD_TO_EMAILS", "greatxproductions@gmail.com"),
}
p.write_text(json.dumps(cfg))
print("patched dist/server/wrangler.json")
PY

echo "=== deploy ==="
npx wrangler deploy
