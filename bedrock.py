import os
import argparse
import logging
import subprocess
import json
from typing import NamedTuple

from docker_util import *

logger = logging.getLogger(__name__)

PROJECTS_ROOT = "/app/projects"
BEDROCK_CONFIG = ".bedrock.conf"

def create_bedrock_project(args):
    name = args.name
    run_docker_cmd(f"bash /app/scripts/create_dev_group.sh", service="dev")
    run_docker_cmd(f"composer create-project roots/bedrock {name}", 
        service="dev", workdir=PROJECTS_ROOT)
    run_docker_cmd(f"chgrp -R developers /app/projects", service="dev")
    run_docker_cmd(f"chmod -R g+rw /app/projects", service="dev")
    with open(BEDROCK_CONFIG, "w") as f: 
        config = {
            "active_project": name, 
            "active_theme":""
        }
        json.dump(config, f, indent=4)

def deploy_bedrock_project(args):
    name = args.name
    if os.path.exists(f"./projects/{name}"):
        run_docker_cmd(f"mkdir -p /www/srv/bedrock", service="web")
        run_docker_cmd(f"rsync -a --exclude node_modules /app/projects/{name} /www/srv/bedrock/", service="web")
        run_docker_cmd(f"python3 /app/scripts/gen_bedrock_config.py {name}", service="web")
        run_docker_cmd(f"python3 /app/scripts/gen_apache_config.py {name}", service="web")
        run_docker_cmd("chown -R www-data:www-data /www/srv/bedrock", service="web")
        run_docker_cmd("a2ensite wordpress", service="web")
        run_docker_cmd("a2enmod rewrite", service="web")
        run_docker_cmd("a2dissite 000-default", service="web")
        run_docker_cmd("service apache2 reload", service="web")
    else:
        raise FileNotFoundError(f"Project {name} not found.")

def load_bedrock_config():
    with open(BEDROCK_CONFIG) as f:
        return json.load(f)

if __name__ == "__main__":
    config = load_bedrock_config()
    print(config)
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="store_true")
    subparsers = parser.add_subparsers(title="Commands", help='Subcommand help.', required=True)
    parser_init = subparsers.add_parser("init", help="Create a new bedrock project")
    parser_init.add_argument("name", help="The name of the project.")
    parser_init.set_defaults(func=create_bedrock_project)

    parser_deploy = subparsers.add_parser("deploy", help="Deploy a project to the web server")
    parser_deploy.add_argument(
        "--name", "-n", 
        default=config.get("active_project"), 
        type=str, 
        help="The name of the project.")
    parser_deploy.set_defaults(func=deploy_bedrock_project)

    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)
    args.func(args)
