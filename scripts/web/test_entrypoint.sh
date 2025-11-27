#!/bin/sh
bash /app/scripts/web/update_dev_permissions.sh
git config --global --add safe.directory "*"
apache2ctl -D FOREGROUND
