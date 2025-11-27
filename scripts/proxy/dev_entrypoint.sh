#!/bin/sh
cp /app/scripts/proxy/app.conf /etc/nginx/conf.d/app.conf
sed -i 's/WEB_HOSTNAME/'$WEB_HOSTNAME'/g' /etc/nginx/conf.d/app.conf
sed -i 's/WEB_PORT/'$WEB_PORT'/g' /etc/nginx/conf.d/app.conf
sed -i 's/PROXY_PORT/'$PROXY_PORT'/g' /etc/nginx/conf.d/app.conf
nginx -c /etc/nginx/nginx.conf -g "daemon off;"