FROM debian:buster

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG BRANCH

ENV REPO="https://github.com/waltage/swe1-app.git"
ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION us-east-1

RUN apt-get update
RUN apt-get install -y wget pkg-config
RUN apt-get install -y git
RUN apt-get install -y build-essential zlib1g-dev \
  libncurses5-dev libgdbm-dev libnss3-dev libssl-dev \
  libsqlite3-dev libreadline-dev libffi-dev curl
RUN apt-get install -y postgresql libpq-dev unzip 
RUN apt-get install -y gcc clang

RUN apt-get install -y systemd nginx sudo
RUN mkdir /xray/
RUN curl https://s3.dualstack.us-east-1.amazonaws.com/aws-xray-assets.us-east-1/xray-daemon/aws-xray-daemon-linux-3.x.zip \
  -o /xray/aws-xray-daemon-linux-3.x.zip
RUN unzip -o /xray/aws-xray-daemon-linux-3.x.zip -d /xray/
RUN cp /xray/xray /usr/bin/xray-daemon


RUN wget -O /usr/local/bin/bazel https://github.com/bazelbuild/bazelisk/releases/download/v1.14.0/bazelisk-linux-amd64
RUN chmod +x "/usr/local/bin/bazel"

RUN rm -rf /var/lib/apt/lists/*

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./init.sh /init.sh

RUN adduser --disabled-password -gecos '' robot
RUN adduser robot sudo
# RUN useradd -ms /bin/bash robot || (addgroup robot && adduser robot -D -G robot)

RUN echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers


USER robot

WORKDIR /home/robot
RUN git clone ${REPO} app
WORKDIR /home/robot/app
RUN git checkout ${BRANCH}

ENTRYPOINT ["/init.sh"]

# docker run -it --rm -p 8000:80 nyu-swe2:latest
# docker run -it --rm --entrypoint="/bin/bash" nyu-swe2:latest