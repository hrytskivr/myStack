#!/bin/sh

# generate tls key & certificate for nginx service
mkdir nginx && \
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout nginx/nginx.key \
            -out nginx/nginx.crt \
            -subj "/C=/ST=/L=/O=/CN=/"

# generate tls key & certificate for registry service
mkdir registry && \
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout registry/registry.key \
            -out registry/registry.crt \
            -subj "/C=/ST=/L=/O=/CN=/"
