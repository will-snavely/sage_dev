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
        f"composer create-project roots/bedrock {name}",
        f"python3 /app/scripts/web/gen_bedrock_config.py {name}",
        f"chgrp -R devs {BEDROCK_ROOT}/{name}",
        f"chown -R www-data {BEDROCK_ROOT}/{name}",
        f"chmod -R g+rw {BEDROCK_ROOT}/{name}",
        workdir=BEDROCK_ROOT,
    )


def deploy_bedrock_project(args):
    name = args.name
    path = f"{BEDROCK_ROOT}/{name}"

    run_docker_cmds(
        f"python3 /app/scripts/web/gen_bedrock_config.py {name}",
        "composer update",
        "composer install",
        user="www-data",
        workdir=f"{BEDROCK_ROOT}/{name}",
        container=args.web_container
    )
    run_docker_cmds(
        f"python3 /app/scripts/web/gen_apache_config.py {name}",
        "a2ensite wordpress",
        "a2enmod rewrite",
        "a2dissite 000-default",
        "service apache2 reload",
        container=args.web_container
    )


def remove_bedrock_project(args):
    name = args.name
    run_docker_cmd(f"rm -rf {BEDROCK_ROOT}/{name}")


def update_dependencies(args):
    name = args.name
    run_docker_cmds(
        "composer update",
        "composer install",
        workdir=f"{BEDROCK_ROOT}/{name}",
        user="www-data"
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument(
        "--web_container",
        "-w",
        type=str,
        help="The name of the project."
    )

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
        type=str,
        help="The name of the project."
    )
    parser_deploy.set_defaults(func=deploy_bedrock_project)

    parser_rm = subparsers.add_parser("rm", help="Remove a project")
    parser_rm.add_argument("name", help="The name of the project.")
    parser_rm.set_defaults(func=remove_bedrock_project)

    parser_update_dep = subparsers.add_parser(
        "update-dep", help="Update composer dependencies"
    )
    parser_update_dep.add_argument(
        "--name",
        "-n",
        type=str,
        help="The name of the project.",
    )
    parser_update_dep.set_defaults(func=update_dependencies)

    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)
    args.func(args)
