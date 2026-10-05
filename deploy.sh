#!/usr/bin/env bash
# Deploy the latest code on the server.
# Push to GitHub from your computer first, then run on the server:
#   cd ~/apps/tabukharajfurniture && ./deploy.sh
set -e
cd "$(dirname "$0")"

echo "[1/4] Pulling latest code from GitHub..."
git pull origin main

echo "[2/4] Installing packages..."
./venv/bin/pip install -q -r requirements.txt

echo "[3/4] Database migrations + static files..."
./venv/bin/python manage.py migrate --noinput
./venv/bin/python manage.py collectstatic --noinput

echo "[4/4] Restarting the app..."
sudo -n systemctl restart tabukharajfurniture.service

sleep 2
CODE=$(curl -s -o /dev/null -w '%{http_code}' -H 'Host: tabukharajfurniture.com' http://127.0.0.1:8006/)
echo "done - site health check: HTTP $CODE"
if [ "$CODE" != "200" ]; then
  echo "WARNING: site did not return 200. Check: sudo systemctl status tabukharajfurniture.service"
  exit 1
fi
