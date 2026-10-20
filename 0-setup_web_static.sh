#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static

# 1. Install Nginx if it is not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update -y
    sudo apt-get install -y nginx
fi

# 2. Create required folders if they don't already exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# 3. Create a fake HTML file to test the Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# 4. Create a symbolic link, deleting and recreating it if it already exists
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# 5. Give recursive ownership of the /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# 6. Update Nginx configuration to serve /data/web_static/current/ to hbnb_static
nginx_config="/etc/nginx/sites-available/default"

# Check if the location block already exists to avoid duplicate entries
if ! grep -q "location /hbnb_static" "$nginx_config"; then
    sudo sed -i 's#server_name _;#server_name _;\n\n    location /hbnb_static {\n        alias /data/web_static/current/;\n    }#' "$nginx_config"
fi

# 7. Restart Nginx after updating the configuration
sudo service nginx restart

exit 0
