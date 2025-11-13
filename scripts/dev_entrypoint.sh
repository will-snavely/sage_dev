bash /app/scripts/update_dev_permissions.sh
git config --system --add safe.directory "*"
apache2ctl -D FOREGROUND
