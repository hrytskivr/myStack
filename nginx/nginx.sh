#!/bin/sh

# check if application is ready
until nc -z app 8000; do
    echo "$(date) - waiting for app..."
    exit 1
done

# start nginx
/usr/sbin/nginx
