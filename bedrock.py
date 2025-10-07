import os
import argparse
import logging
import subprocess
import json
from typing import NamedTuple

from docker_util import *

logger = logging.getLogger(__name__)


def create_bedrock_project(args):
    name = args.name
    run_docker_cmds(
        "bash /app/scripts/update_dev_user.sh",
        f"composer create-project roots/bedrock {name}", 
        f"python3 /app/scripts/gen_bedrock_config.py {name}",
        f"chgrp -R devs {BEDROCK_ROOT}",
        f"chown -R www-data {BEDROCK_ROOT}",
        f"chmod -R g+rw {BEDROCK_ROOT}",
        workdir=BEDROCK_ROOT
    )
    save_bedrock_config({"working_project": name, "working_theme": ""})


def deploy_bedrock_project(args):
    name = args.name
    if os.path.exists(f"./projects/{name}"):
        run_docker_cmd(f"chown -R www-data {BEDROCK_ROOT}")

        run_docker_cmds(
            "composer update",
            "composer install",
            f"chgrp -R devs {BEDROCK_ROOT}",
            f"chmod -R g+rw {BEDROCK_ROOT}",
            workdir=f"{BEDROCK_ROOT}/{name}", 
            user="www-data"
        )
        run_docker_cmds(
            f"python3 /app/scripts/gen_apache_config.py {name}",
            "a2ensite wordpress",
            "a2enmod rewrite",
            "a2dissite 000-default",
            "service apache2 reload"
        )
    else:
        raise FileNotFoundError(f"Project {name} not found.")


if __name__ == "__main__":
    config = load_bedrock_config()
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="store_true")
    subparsers = parser.add_subparsers(
        title="Commands", help="Subcommand help.", required=True
    )
    parser_init = subparsers.add_parser("init", help="Create a new bedrock project")
    parser_init.add_argument("name", help="The name of the project.")
    parser_init.set_defaults(func=create_bedrock_project)

    parser_deploy = subparsers.add_parser(
        "deploy", help="Deploy a project to the web server"
    )
    parser_deploy.add_argument(
        "--name",
        "-n",
        default=config.get("working_project"),
        type=str,
        help="The name of the project.",
    )
    parser_deploy.set_defaults(func=deploy_bedrock_project)

    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)
    logger.debug(f"Configuration: {config}")
    args.func(args)
