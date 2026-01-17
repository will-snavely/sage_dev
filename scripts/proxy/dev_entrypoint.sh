#!/bin/sh
rm -rf /etc/nginx/conf.d/default.conf

if [ "$USE_HTTPS" = "1" ]; then
    cp /app/scripts/proxy/app.https.conf /etc/nginx/conf.d/app.conf
else
    cp /app/scripts/proxy/app.http.conf /etc/nginx/conf.d/app.conf
fi

sed -i 's/WEB_HOSTNAME/'$WEB_HOSTNAME'/g' /etc/nginx/conf.d/app.conf
sed -i 's/WEB_PORT/'$WEB_PORT'/g' /etc/nginx/conf.d/app.conf
sed -i 's/PROXY_PORT_HTTPS/'$PROXY_PORT_HTTPS'/g' /etc/nginx/conf.d/app.conf
sed -i 's/PROXY_PORT_HTTP/'$PROXY_PORT_HTTP'/g' /etc/nginx/conf.d/app.conf
nginx -c /etc/nginx/nginx.conf -g "daemon off;"
