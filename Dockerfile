FROM python:alpine3.17
COPY my_python /bin/my_python
COPY root /var/spool/cron/crontabs/root
RUN chmod +x /bin/my_python
CMD crond -l 2 -f
