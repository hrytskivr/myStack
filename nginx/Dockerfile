FROM ubuntu:trusty

# install nginx
RUN apt-get update && \
    apt-get install -y nginx=1.4.6-1ubuntu3.8

# clean apt data
RUN apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# turn off nginx daemon & replace default config
RUN echo 'daemon off;' >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/ /etc/nginx/sites-enabled

ENTRYPOINT '/usr/sbin/nginx'