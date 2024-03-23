#!/usr/bin/env bash
# sets up web servers

if [ ! -x /usr/sbin/nginx ]; then
    apt-get update
    apt-get -y upgrade
    apt-get -y install nginx
fi

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

echo "Hello Word !" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data

sed -i '/listen 80 default_server;/a \\tlocation /hbnb_static/ { \n\t\t alias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

service nginx restart
