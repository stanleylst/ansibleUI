#!/bin/bash

cat << EOF > /tmp/CrondRebuild.txt
IFA_ENV=${IFA_ENV}
LANG=zh_CN.UTF-8
LC_CTYPE=zh_CN.UTF-8

# @sunyifei 一号通身份验证接口检测
*/1 * * * * ./etc/profile;cd /opt/script; ./alarm_yht.sh > /dev/null 2>&1

EOF

php /srv/www/king-gw/vendor/king/core/bin/printCrontab.php >> /tmp/CrondRebuild.txt

crontab  -uwww /tmp/CrondRebuild.txt   
