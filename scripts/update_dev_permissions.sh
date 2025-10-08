if ! getent group devs >/dev/null; then
    groupadd -g "$DEV_GROUP_ID" devs
    usermod -aG devs www-data
    chgrp -R /www devs
fi
