FROM ubuntu:trusty

# install nginx
RUN apt-get update && \
    apt-get install -y nginx=1.4.6-1ubuntu3.8

# clean apt data
RUN apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# turn off nginx daemon, replace default config & copy over entrypoint script
WORKDIR /etc/nginx
RUN echo "daemon off;" >> nginx.conf
RUN rm -rf sites-enabled
ADD . /etc/nginx
