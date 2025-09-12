import argparse
import subprocess
import collections
import os
import sys
import json
import logging
import shlex

WORDPRESS_ROOT = "/srv/www/wordpress"
THEMES_ROOT = f"{WORDPRESS_ROOT}/wp-content/themes"

logger = logging.getLogger(__name__)

def docker_cmd(cmd, service, user, workdir):
    result = ["docker-compose", "exec"]
    result += ["--user", user] if user else []
    result += ["--workdir", workdir] if workdir else [] 
    result += [service] 
    result += shlex.split(cmd) if isinstance(cmd, str) else list(cmd)
    return result

def log_docker_cmd(cmd, level=logging.DEBUG, *args, **kwargs):
    msg = "(docker call) " + shlex.join(cmd)
    logger.log(level, msg)

def run_docker_cmd(cmd, service="web", user="www-data", workdir=WORDPRESS_ROOT):
    dcmd = docker_cmd(cmd, service=service, user=user, workdir=workdir)
    log_docker_cmd(dcmd)
    return subprocess.run(dcmd)

def list_themes(args):
    run_docker_cmd("wp theme list")

def activate_theme(args):
    run_docker_cmd(f"wp theme activate {args.name}")

def build_sage_theme(args):
    run_docker_cmd("composer update", workdir=f"{THEMES_ROOT}/{args.name}")
    run_docker_cmd("npm install", workdir=f"{THEMES_ROOT}/{args.name}")
    run_docker_cmd("npm run build", workdir=f"{THEMES_ROOT}/{args.name}")
    run_docker_cmd(f"chown -R www-data:www-data {args.name}", 
                   user="root", workdir=THEMES_ROOT)

def create_sage_theme(args):
    name = args.name
    themes_dir = f"{WORDPRESS_ROOT}/wp-content/themes"
    run_docker_cmd(f"composer create-project roots/sage {name}", 
                   user="root", workdir=themes_dir)
    run_docker_cmd(f"chown -R www-data:www-data {name}", 
                   user="root", workdir=themes_dir)
    run_docker_cmd(f"chmod -R g+rw {name}", 
                   user="root", workdir=themes_dir)

    search = r"\/app\/themes\/sage\/public\/build\/"
    replace = r"\/wp-content\/themes\/" + name + r"\/public\/build\/"
    run_docker_cmd(f"sed -i 's/{search}/{replace}/g' {name}/vite.config.js", workdir=themes_dir)

def exec_command(args):
    if args.workdir:
        workdir = args.workdir
    run_docker_cmd(args.command, workdir=workdir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="store_true")

    subparsers = parser.add_subparsers(title="Commands", help='Subcommand help.')
    parser_init = subparsers.add_parser("init", help="Create a new sage theme on the container.")
    parser_init.add_argument("name", type=str, help="The name of the theme.")
    parser_init.set_defaults(func=create_sage_theme)

    parser_init = subparsers.add_parser("build", help="Build a sage theme on the container.")
    parser_init.add_argument("name", type=str, help="The name of the theme.")
    parser_init.set_defaults(func=build_sage_theme)

    parser_list = subparsers.add_parser("list", help="List themes installed on the container.")
    parser_list.set_defaults(func=list_themes)

    parser_list = subparsers.add_parser("activate", help="Activate a theme on the container.")
    parser_list.set_defaults(func=activate_theme)

    parser_exec = subparsers.add_parser("exec", help="Execute a command on the container")
    parser_exec.add_argument("--workdir", "-w", default=WORDPRESS_ROOT, type=str, help="Working directory.")
    parser_exec.add_argument("command", nargs=argparse.REMAINDER)
    parser_exec.set_defaults(func=exec_command)

    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)
    args.func(args)
