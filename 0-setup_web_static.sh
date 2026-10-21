#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static

id ubuntu &>/dev/null || useradd -m ubuntu

if ! dpkg -s nginx &> /dev/null; then
    apt-get update
    apt-get -y install nginx
fi

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

echo "<html>
  <head>
  </head>
  <body>
    School
  </body>
</html>" > /data/web_static/releases/test/index.html

if [ -L /data/web_static/current ]; then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

if ! grep -q "location /hbnb_static" /etc/nginx/sites-available/default; then
    sed -i '/server_name _;/a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default
fi

service nginx restart

exit 0
