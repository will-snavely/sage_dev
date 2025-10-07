import os
import secrets
import collections
import argparse

apache_config = """
<VirtualHost *:80>
    DocumentRoot {wp_root}
    <Directory {wp_root}>
        Options FollowSymLinks
        AllowOverride Limit Options FileInfo
        DirectoryIndex index.php
        Require all granted
    </Directory>
    <Directory {wp_root}/wp-content>
        Options FollowSymLinks
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
    with open("/etc/apache2/sites-available/wordpress.conf", "w") as f:
        f.write(apache_config.format(wp_root=web_root))
