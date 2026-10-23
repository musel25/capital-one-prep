#!/usr/bin/env bash
# Publish only compiled static assets. Attempts and notes never leave this PC.
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ -n "$(git status --porcelain)" ]]; then
  echo 'Commit and push the reviewed changes before deploying.' >&2
  exit 1
fi
commit=$(git rev-parse --short=12 HEAD)
release="/var/www/capital-one-prep/releases/${commit}-$(date -u +%Y%m%dT%H%M%S)"
npm test
npm run build
ssh -o BatchMode=yes my-vps bash -s -- "$release" <<'PREPARE'
set -euo pipefail
sudo -n install -d -m 755 -o "$(id -un)" -g "$(id -gn)" \
  /var/www/capital-one-prep /var/www/capital-one-prep/releases "$1"
PREPARE
rsync -az --chmod=D755,F644 dist/ "my-vps:$release/"
ssh -o BatchMode=yes my-vps bash -s -- "$release" <<'REMOTE'
set -euo pipefail
release=$1
current=/var/www/capital-one-prep/current
config=/etc/nginx/sites-available/timer.musel.dev
backup="${config}.capital-one-backup-$(date -u +%Y%m%dT%H%M%S)"
previous=$(readlink "$current" || true)
sudo cp -p "$config" "$backup"
rollback() {
  echo 'Deployment failed; restoring previous release and nginx configuration.' >&2
  if [[ -n "$previous" ]]; then
    ln -sfn "$previous" "${current}.rollback"
    mv -Tf "${current}.rollback" "$current"
  else
    rm -f "$current"
  fi
  sudo cp -p "$backup" "$config"
  sudo nginx -t && sudo systemctl reload nginx
}
trap rollback ERR
if ! grep -Fq 'location ^~ /grind/capital-one/' "$config"; then
  config_temp=$(mktemp)
  awk '
    /# Grind Recall static application/ {
      print "    # Capital One preparation static application"
      print "    location = /grind/capital-one { return 301 /grind/capital-one/; }"
      print "    location ^~ /grind/capital-one/ {"
      print "        alias /var/www/capital-one-prep/current/;"
      print "        index index.html;"
      print "        expires -1;"
      print "    }"
      inserted=1
    }
    { print }
    END { if (!inserted) exit 2 }
  ' "$config" > "$config_temp"
  sudo install -m 644 "$config_temp" "$config"
  rm -f "$config_temp"
fi
ln -sfn "$release" "${current}.next"
mv -Tf "${current}.next" "$current"
sudo nginx -t
sudo systemctl reload nginx
curl -fsS https://timer.musel.dev/grind/capital-one/ | grep -Fq '<title>Capital One Prep'
curl -fsS https://timer.musel.dev/grind/ >/dev/null
curl -fsS https://timer.musel.dev/api/health | grep -Fq '"ok":true'
trap - ERR
echo "Published $release"
echo "Nginx backup: $backup"
REMOTE
echo 'https://timer.musel.dev/grind/capital-one/'
