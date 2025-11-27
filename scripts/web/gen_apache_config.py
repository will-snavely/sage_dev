import os
import secrets
import collections
import argparse

apache_config = """
<VirtualHost *:{web_port}>
    ServerName {web_service_name}
    DocumentRoot {wp_root}
    <Directory {wp_root}>
        Options FollowSymLinks
        AllowOverride All
        DirectoryIndex index.php
        Require all granted
    </Directory>
</VirtualHost>
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="The bedrock project name.")
    args = parser.parse_args()
    bedrock_root = os.environ["BEDROCK_ROOT"]
    web_root = f"{bedrock_root}/{args.name}/web/"
    web_port=os.environ["WEB_PORT"]

    with open("/etc/apache2/sites-available/wordpress.conf", "w") as f:
        f.write(apache_config.format(
            wp_root=web_root, 
            web_service_name="web", 
            web_port=web_port))
