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
exec su -s /bin/sh www-data -c "apache2ctl -D FOREGROUND"
