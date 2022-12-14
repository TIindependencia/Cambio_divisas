FROM python:alpine3.17

RUN apk add --no-cache curl gcc g++ unixodbc-dev \
    && pip3 install --upgrade pip \
    && pip3 install pandas

COPY my_python /bin/my_python
COPY root /var/spool/cron/crontabs/root
RUN chmod +x /bin/my_python
CMD crond -l 2 -f

COPY /requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
