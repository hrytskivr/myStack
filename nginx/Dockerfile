FROM ubuntu:trusty

# install nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# turn it off, replace default config and turn back on
RUN echo 'daemon off;' >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/ /etc/nginx/sites-enabled

ENTRYPOINT '/usr/sbin/nginx'