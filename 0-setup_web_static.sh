#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static

if ! command -v nginx &> /dev/null; then
    apt-get update -y
    apt-get install -y nginx
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

nginx_config="/etc/nginx/sites-available/default"
if ! grep -q "location /hbnb_static" "$nginx_config"; then
    sed -i 's#server_name _;#server_name _;\n\n    location /hbnb_static {\n        alias /data/web_static/current/;\n    }#' "$nginx_config"
fi

service nginx restart

exit 0
