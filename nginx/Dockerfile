FROM ubuntu:trusty

# install nginx & openssl
RUN apt-get update && \
    apt-get install -y nginx=1.4.6-1ubuntu3.8 && \
    apt-get install -y openssl=1.0.1f-1ubuntu2.23

# clean apt data
RUN apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# turn off nginx daemon & replace default config
RUN echo 'daemon off;' >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/ /etc/nginx/sites-enabled

# generate key & certificate
RUN mkdir /tls
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
                -keyout /tls/my.app.key -out /tls/my.app.crt \
                -subj '/C=/ST=/L=/O=/CN=/'

ENTRYPOINT '/usr/sbin/nginx'