#!/bin/sh
if ! getent group devs >/dev/null; then
	groupadd -g "$DEV_GROUP_ID" devs
fi
usermod -aG devs www-data
chgrp devs /www/srv
chmod g+s /www/srv

# Composer (run as www-data) needs a writable cache dir under its home;
# without it, every install re-downloads all packages and the automatic
# dist->source fallback fails outright instead of just being slow.
mkdir -p /var/www/.cache/composer
chown -R www-data:www-data /var/www/.cache

# web/.htaccess is hand-authored for Bedrock's directory layout (WordPress's
# own generator has no idea wp-admin/wp-includes live under web/wp/ or that
# wp-content is remapped to web/app/). Make it read-only to www-data so a
# hard flush_rules() call — from wp-admin's Permalinks page, a plugin, etc. —
# can't silently overwrite it with the generic single-site block. Production
# already gets this for free (root-owned, Apache runs as www-data); this just
# makes dev behave the same way on purpose instead of by accident.
if [ -f "/www/srv/$PROJECT/web/.htaccess" ]; then
	chown root:root "/www/srv/$PROJECT/web/.htaccess"
	chmod 444 "/www/srv/$PROJECT/web/.htaccess"
fi
