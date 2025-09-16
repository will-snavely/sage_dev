import os
import argparse
import logging
import subprocess

from docker_util import *

logger = logging.getLogger(__name__)

PROJECTS_ROOT = "/app/projects"

def create_bedrock_project(args):
    name = args.name
    run_docker_cmd(f"bash /app/scripts/create_dev_group.sh", service="dev")
    run_docker_cmd(f"composer create-project roots/bedrock {name}", 
        service="dev", workdir=PROJECTS_ROOT)
    run_docker_cmd(f"chgrp -R developers /app/projects", service="dev")
    run_docker_cmd(f"chmod -R g+rw /app/projects", service="dev")

def deploy_bedrock_project(args):
    name = args.name
    if os.path.exists(f"./projects/{name}"):
        run_docker_cmd(f"mkdir -p /www/srv/bedrock", service="web")
        run_docker_cmd(f"cp -rf /app/projects/{name} /www/srv/bedrock", service="web")
        run_docker_cmd(f"python3 /app/scripts/gen_bedrock_config.py {name}", service="web")
        run_docker_cmd(f"python3 /app/scripts/gen_apache_config.py {name}", service="web")
        run_docker_cmd("chown -R www-data:www-data /www/srv/bedrock", service="web")
        run_docker_cmd("a2ensite wordpress", service="web")
        run_docker_cmd("a2enmod rewrite", service="web")
        run_docker_cmd("a2dissite 000-default", service="web")
        run_docker_cmd("service apache2 reload", service="web")
    else:
        raise FileNotFoundError(f"Project {name} not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="store_true")
    subparsers = parser.add_subparsers(title="Commands", help='Subcommand help.', required=True)
    parser_init = subparsers.add_parser("init", help="Create a new bedrock project")
    parser_init.add_argument("name", type=str, help="The name of the project.")
    parser_init.set_defaults(func=create_bedrock_project)

    parser_init = subparsers.add_parser("deploy", help="Deploy a project to the web server")
    parser_init.add_argument("name", type=str, help="The name of the project.")
    parser_init.set_defaults(func=deploy_bedrock_project)

    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)
    args.func(args)
