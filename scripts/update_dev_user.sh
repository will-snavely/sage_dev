CUR_DEV_GROUP_ID=$(getent group devs | cut -d: -f3)
CUR_DEV_USER_ID=$(id -u dev)
if [[ "$CUR_DEV_GROUP_ID" -ne "$DEV_GROUP_ID" ]]; then 
    groupmod -g "$DEV_GROUP_ID" devs
    find /home -group "$CUR_DEV_GROUP_ID" -exec chgrp -h devs {} \; > /dev/null 2>&1
    find /www -group "$CUR_DEV_GROUP_ID" -exec chgrp -h devs {} \; > /dev/null 2>&1
fi
if [[ "$CUR_DEV_USER_ID" -ne "$DEV_USER_ID" ]]; then 
    usermod -u $DEV_USER_ID dev
    find /home -group "$CUR_DEV_GROUP_ID" -exec chgrp -h devs {} \; > /dev/null 2>&1
    find /www -group "$CUR_DEV_GROUP_ID" -exec chgrp -h devs {} \; > /dev/null 2>&1
fi
