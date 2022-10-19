FROM debian:buster

ENV REPO="https://github.com/waltage/swe1-app.git"


RUN useradd -ms /bin/bash robot || (addgroup robot && adduser robot -D -G robot)

RUN apt-get update
RUN apt-get install -y wget pkg-config
RUN apt-get install -y git
RUN apt-get install -y build-essential zlib1g-dev \
  libncurses5-dev libgdbm-dev libnss3-dev libssl-dev \
  libsqlite3-dev libreadline-dev libffi-dev curl
RUN rm -rf /var/lib/apt/lists/*

RUN wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tar.xz
RUN tar -xf Python-3.8.12.tar.xz
RUN mv Python-3.8.12 /opt/Python-3.8.12


WORKDIR /opt/Python-3.8.12
RUN ./configure --enable-optimizations --enable-shared
RUN make
RUN make altinstall
RUN ldconfig /opt/Python-3.8.12

WORKDIR /

# RUN wget -O /usr/local/bin/bazel https://github.com/bazelbuild/bazelisk/releases/download/v1.14.0/bazelisk-linux-amd64

RUN wget -O /usr/local/bin/bazel https://github.com/bazelbuild/bazelisk/releases/download/v1.14.0/bazelisk-linux-arm64
RUN chmod +x "/usr/local/bin/bazel"

USER robot
WORKDIR /home/robot



RUN git clone ${REPO} app
WORKDIR /home/robot/app
RUN git checkout deployment

ENTRYPOINT ["/bin/bash"]

# docker run -it --rm nyu-swe2:latest