#!/bin/bash

echo "Starting nginx"
sudo service nginx start || (echo "Error with nginx" && exit)
sudo xray-daemon -f /var/log/xray-daemon.log &

bazel run //shortlist/backend:serve
