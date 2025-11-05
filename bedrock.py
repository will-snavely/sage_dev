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
        f"python3 /app/scripts/gen_bedrock_config.py {name}",
        f"chgrp -R devs {BEDROCK_ROOT}/{name}",
        f"chown -R www-data {BEDROCK_ROOT}/{name}",
        f"chmod -R g+rw {BEDROCK_ROOT}/{name}",
        workdir=BEDROCK_ROOT,
    )
    save_bedrock_config({"working_project": name, "working_theme": ""})


def deploy_bedrock_project(args):
    name = args.name
    if os.path.exists(f"./projects/{name}"):
        run_docker_cmds(
            f"python3 /app/scripts/gen_bedrock_config.py {name}",
            "composer update",
            "composer install",
            workdir=f"{BEDROCK_ROOT}/{name}",
            user="www-data"
        )
        run_docker_cmds(
            f"python3 /app/scripts/gen_apache_config.py {name}",
            "a2ensite wordpress",
            "a2enmod rewrite",
            "a2dissite 000-default",
            "service apache2 reload",
            workdir=f"{BEDROCK_ROOT}/{name}",
        )
    else:
        raise FileNotFoundError(f"Project {name} not found.")


def remove_bedrock_project(args):
    name = args.name
    run_docker_cmd(f"rm -rf {BEDROCK_ROOT}/{name}")


def update_dependencies(args):
    name = args.name
    if os.path.exists(f"./projects/{name}"):
        run_docker_cmds(
            "composer update",
            "composer install",
            workdir=f"{BEDROCK_ROOT}/{name}",
            user="www-data"
        )


def run_tests(args):
    name = args.name
    if os.path.exists(f"./projects/{name}"):
        run_docker_cmds(
            "./vendor/bin/phpunit web/app/tests",
            workdir=f"{BEDROCK_ROOT}/{name}"
        )


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

    parser_rm = subparsers.add_parser("rm", help="Remove a project")
    parser_rm.add_argument("name", help="The name of the project.")
    parser_rm.set_defaults(func=remove_bedrock_project)

    parser_update_dep = subparsers.add_parser(
        "update-dep", help="Update composer dependencies"
    )
    parser_update_dep.add_argument(
        "--name",
        "-n",
        default=config.get("working_project"),
        type=str,
        help="The name of the project.",
    )
    parser_update_dep.set_defaults(func=update_dependencies)

    parser_test = subparsers.add_parser(
        "test", help="Run test suite"
    )
    parser_test.add_argument(
        "--name",
        "-n",
        default=config.get("working_project"),
        type=str,
        help="The name of the project.",
    )
    parser_test.set_defaults(func=run_tests)

    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)
    logger.debug(f"Configuration: {config}")
    args.func(args)
