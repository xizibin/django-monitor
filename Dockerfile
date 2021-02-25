FROM python:3.8.8-alpine3.13

LABEL MAINTAINER NAMTUA

EXPOSE 8000

WORKDIR /doan

COPY . /doan

RUN pip3 install -r requirements.txt && rm -rf /var/cache/apk/* 

CMD [ "python3", "manage.py", "runserver" ]


