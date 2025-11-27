#!/bin/sh
bash /app/scripts/web/update_dev_permissions.sh
grep -q "Listen 8080" /etc/apache2/ports.conf || echo "Listen 8080" | tee -a /etc/apache2/ports.conf
git config --system --add safe.directory "*"
apache2ctl -D FOREGROUND
