if ! getent group "$DEV_GROUP_ID" > /dev/null; then
    groupadd -g "$DEV_GROUP_ID" developers
fi
