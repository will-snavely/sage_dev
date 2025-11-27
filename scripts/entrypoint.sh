#!/bin/sh
python3 /app/scripts/web/gen_bedrock_config.py $PROJECT_NAME
python3 /app/scripts/web/gen_apache_config.py $PROJECT_NAME
a2ensite wordpress
a2enmod rewrite
a2dissite 000-default
service apache2 reload
apache2ctl -D FOREGROUND
