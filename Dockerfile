FROM debian:bullseye

RUN apt-get update
RUN apt-get -y install python3 postgresql python3-pip

RUN apt-get -y install systemctl
RUN apt-get -y install nginx
RUN pip3 install django psycopg gunicorn

COPY ./root/ /

# nginx reverse proxy start
RUN systemctl enable nginx
RUN systemctl start nginx


EXPOSE 80
RUN chmod +x /init.sh
ENTRYPOINT ["/bin/bash", "/init.sh"]

