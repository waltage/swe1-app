#!/bin/bash

echo "Starting nginx"
sudo service nginx start || (echo "Error with nginx" && exit)
sudo xray-daemon -f /var/log/xray-daemon.log &

bazel run //shortlist/backend:manage -- migrate
bazel run //shortlist/backend:manage -- collectstatic --noinput
bazel run //shortlist/backend:serve
