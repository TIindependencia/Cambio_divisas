FROM python:alpine3.17
COPY my_python /bin/my_python
COPY root /var/spool/cron/crontabs/root
RUN chmod +x /bin/my_python
CMD crond -l 2 -f
RUN pip install -r pyodbc
RUN pip install -r pandas
RUN pip install -r requests
RUN pip install -r pytz
RUN pip install -r pypyodbc
