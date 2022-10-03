#!/bin/bash
systemctl start nginx

cd /app/hello
gunicorn hello.wsgi -b localhost:8080

echo "error with gunicorn exit"
tail -f /dev/null