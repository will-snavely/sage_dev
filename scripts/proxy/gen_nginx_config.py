import os
import secrets
import collections
import argparse

nginx_config = """
server {
    listen {proxy_port};
    server_name {web_hostname}; 

    location / {
        proxy_pass http://{web_service_name}:{web_port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""

if __name__ == "__main__":
    web_hostname = os.environ["WEB_HOSTNAME"]
    proxy_port = os.environ["PROXY_PORT"]
    web_port=os.environ["WEB_PORT"]
    with open("/etc/nginx/conf.d/app.conf", "w") as f:
        f.write(nginx_config.format(
            proxy_port=proxy_port,
            web_service_name="web",
            web_hostname=web_hostname,
            web_port=web_port
        ))
