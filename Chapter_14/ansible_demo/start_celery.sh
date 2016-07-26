process=`ps -ef |grep -E "./manage.py celery worker -c 10 --autoreload"|awk '{print $2}'`
redis-cli config set stop-writes-on-bgsave-error no
for i in $process;
do
    if [ $i -eq 1 ]; then
        echo "do nothing"
    else
        kill -9 $i
    fi
done
./manage.py celery purge -f;./manage.py celery worker -c 10 --autoreload
