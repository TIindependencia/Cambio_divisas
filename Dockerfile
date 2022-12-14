FROM python:alpine3.17

RUN apk add --no-cache curl gcc g++ unixodbc-dev

COPY my_python /bin/my_python
COPY root /var/spool/cron/crontabs/root
RUN chmod +x /bin/my_python
CMD crond -l 2 -f

RUN pip3 install pyodbc
RUN pip3 install pandas
RUN pip3 install requests
RUN pip3 install pytz
RUN pip3 install pypyodbc
