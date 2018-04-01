#!/bin/sh

# deploy local docker registry
docker container run -d -p 5000:5000 --name registry --hostname registry \
                     --restart unless-stopped --network %APP_NAME%_network \
                     -v $(pwd)/store:/var/lib/registry \
                     -v $(pwd)/../tls/registry:/tls \
                     -e REGISTRY_HTTP_TLS_KEY=/tls/registry.key \
                     -e REGISTRY_HTTP_TLS_CERTIFICATE=/tls/registry.crt \
                     registry:2.6
