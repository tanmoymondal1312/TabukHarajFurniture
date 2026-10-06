#!/usr/bin/env bash
# Deploy the latest code on the server.
# Push to GitHub from your computer first, then run on the server:
#   cd ~/apps/tabukharajfurniture && ./deploy.sh
set -e
cd "$(dirname "$0")"

echo "[1/5] Pulling latest code from GitHub..."
git pull origin main

echo "[2/5] Installing packages..."
./venv/bin/pip install -q -r requirements.txt

echo "[3/5] Database migrations + static files..."
./venv/bin/python manage.py migrate --noinput
./venv/bin/python manage.py collectstatic --noinput

echo "[4/5] Restarting the app..."
sudo -n systemctl restart tabukharajfurniture.service

sleep 2
CODE=$(curl -s -o /dev/null -w '%{http_code}' -H 'Host: tabukharajfurniture.com' http://127.0.0.1:8006/)
echo "done - site health check: HTTP $CODE"
if [ "$CODE" != "200" ]; then
  echo "WARNING: site did not return 200. Check: sudo systemctl status tabukharajfurniture.service"
  exit 1
fi

echo "[5/5] Purging Cloudflare cache..."
TOKEN=$(awk -F'= ' '/dns_cloudflare_api_token/{print $2}' "$HOME/apps/_configs/cf-tabuk.ini" 2>/dev/null || true)
if [ -n "$TOKEN" ]; then
  PURGE=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/6f3fb3ef365015d4493d191632b8f2e1/purge_cache" \
    -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
    -d '{"purge_everything":true}' || true)
  case "$PURGE" in
    *'"success":true'*) echo "Cloudflare cache purged" ;;
    *) echo "WARNING: Cloudflare purge did not confirm success" ;;
  esac
else
  echo "WARNING: CF token not found in ~/apps/_configs/cf-tabuk.ini - cache not purged"
fi
