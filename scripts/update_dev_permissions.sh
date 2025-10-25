if ! getent group devs >/dev/null; then
    groupadd -g "$DEV_GROUP_ID" devs
fi
usermod -aG devs www-data
chgrp -R devs /www
