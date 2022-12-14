FROM python:alpine3.17

RUN apk --no-cache --update-cache add curl gcc g++ unixodbc-dev python3 py3-pip py3-arrow  py3-pandas \
    && pip3 install --upgrade pip 

COPY my_python /bin/my_python
COPY root /var/spool/cron/crontabs/root
RUN chmod +x /bin/my_python
CMD crond -l 2 -f

COPY /requirements.txt /requirements.txt
RUN pip --no-cache-dir install -r /requirements.txt
