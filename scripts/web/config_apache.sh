
#!/bin/sh
python3 /app/scripts/web/gen_apache_config.py $PROJECT_NAME
grep -q "Listen $WEB_PORT" /etc/apache2/ports.conf || echo "Listen $WEB_PORT" | tee -a /etc/apache2/ports.conf
a2ensite wordpress
a2enmod rewrite
a2dissite 000-default
service apache2 reload
