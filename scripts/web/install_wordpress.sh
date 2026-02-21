if wp core is-installed --quiet; then
  echo "✔ WordPress is already installed. Skipping core install."
else
  echo "Installing WordPress..."
  wp core install \
    --url="${WP_HOME}" \
    --title=${WP_SITE_TITLE} \
    --admin_user=${WP_ADMIN_USER} \
    --admin_password="$(cat ${WP_ADMIN_PASSWORD_FILE})" \
    --admin_email=${WP_ADMIN_EMAIL} \
    --skip-email
fi
