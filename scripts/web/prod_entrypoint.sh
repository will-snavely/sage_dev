#!/bin/sh
# Activates the (already-generated, bind-mounted) apache vhost config on
# every container start, so a plain container restart/recreate is enough to
# come back up correctly - no manual "task config-apache" required. Runs as
# root because a2ensite/a2enmod/ports.conf need it; apache itself is then
# started as www-data to match the image's no-privilege-separation setup
# (see the chown of /var/run/apache2 etc. in the Dockerfile).
set -e
grep -q "Listen $WEB_PORT" /etc/apache2/ports.conf || echo "Listen $WEB_PORT" | tee -a /etc/apache2/ports.conf
a2ensite wordpress
a2enmod rewrite
a2dissite 000-default

# web/app/cache isn't a persisted volume, so it's gone every time this
# container is recreated (deploy, restart: always, host reboot, ...) and has
# to be rebuilt from nothing. Acorn (theme bootstrap) lazily recreates its
# subdirectories under here on the first request via an is_dir()-then-mkdir()
# check that isn't race-safe: if two requests hit a freshly-started container
# at once, they can both see the directory missing and both call mkdir(),
# and the loser's "File exists" warning gets turned into a fatal
# ErrorException by Acorn's error handling, 500-ing that request. Creating
# the tree here - before apache is even started, so before any traffic can
# possibly arrive - closes that window: Acorn's per-request check just finds
# the directories already there and never calls mkdir() at all.
ACORN_CACHE_DIR="$BEDROCK_ROOT/$PROJECT/web/app/cache/acorn"
mkdir -p \
    "$ACORN_CACHE_DIR/framework/cache/data" \
    "$ACORN_CACHE_DIR/framework/views" \
    "$ACORN_CACHE_DIR/framework/sessions" \
    "$ACORN_CACHE_DIR/logs"
chown -R www-data:www-data "$BEDROCK_ROOT/$PROJECT/web/app/cache"

exec su -s /bin/sh www-data -c "apache2ctl -D FOREGROUND"
