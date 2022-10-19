FROM ubuntu:bionic

ENV REPO="https://github.com/waltage/swe1-app.git"


RUN useradd -ms /bin/bash robot || (addgroup robot && adduser robot -D -G robot)

RUN apt-get update
RUN apt-get install -y wget pkg-config
RUN apt-get install -y git

RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update
RUN apt-get install -y python3.8

RUN rm -rf /var/lib/apt/lists/*

# RUN wget -O /usr/local/bin/bazel https://github.com/bazelbuild/bazelisk/releases/download/v1.14.0/bazelisk-linux-amd64

RUN wget -O /usr/local/bin/bazel https://github.com/bazelbuild/bazelisk/releases/download/v1.14.0/bazelisk-linux-arm64

RUN chmod +x "/usr/local/bin/bazel"

USER robot
WORKDIR /home/robot

# RUN mv bazelisk-linux-amd64 "/usr/local/bin/bazel"

RUN git clone ${REPO} app
WORKDIR /home/robot/app

ENTRYPOINT ["/bin/bash"]

# docker run -it --rm nyu-swe2:latest