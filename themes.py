import argparse
import subprocess
import collections
import os
import sys
import json
import logging

def list_themes(args):
    command = [
        "docker-compose", "exec",
        "--workdir", "/srv/www/wordpress",
        "--user", "www-data",
        "web",
        "wp", "theme", "list"]
    print(" ".join(command))
    result = subprocess.run(command)

def build_sage_theme(args):
    name = args.name
    theme_dir = f"/srv/www/wordpress/wp-content/themes/{name}"
    base_cmd =  ["docker-compose", "exec", "--workdir", theme_dir, "web"]

    npm_install = base_cmd + ["bash", "-c", "npm install"]
    logging.info(" ".join(npm_install))
    result = subprocess.run(npm_install)

    npm_build = base_cmd + ["npm", "run", "build"]
    logging.info(" ".join(npm_build))
    result = subprocess.run(npm_build)

def create_sage_theme(args):
    cwd = os.getcwd()
    name = args.name
    host_theme_dir = os.path.join(cwd, "themes", name)
    web_themes_dir = "/srv/www/wordpress/wp-content/themes"
    os.makedirs(host_theme_dir, exist_ok=True)
    base_cmd =  ["docker-compose", "exec", "--workdir", web_themes_dir, "web"]

    sage_cmd = base_cmd + ["composer", "create-project", "roots/sage", name]
    logging.info(" ".join(sage_cmd))
    result = subprocess.run(sage_cmd)

    chown_cmd = base_cmd + ["chown", "-R", "www-data:www-data", name]
    logging.info(" ".join(chown_cmd))
    result = subprocess.run(chown_cmd)

    chmod_cmd = base_cmd + ["chmod", "-R", "g+rw", name]
    logging.info(" ".join(chmod_cmd))
    result = subprocess.run(chmod_cmd)

    search = r"\/app\/themes\/sage\/public\/build\/"
    replace = r"\/wp-content\/themes\/" + name + r"\/public\/build\/"
    sed_cmd = base_cmd + ["sed", "-i", f"s/{search}/{replace}/g", f"{name}/vite.config.js"]
    print(" ".join(sed_cmd))
    result = subprocess.run(sed_cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="Commands", help='Subcommand help.')
    parser_init = subparsers.add_parser("init", help="Create a new sage theme on the container.")
    parser_init.add_argument("name", type=str, help="The name of the theme.")
    parser_init.set_defaults(func=create_sage_theme)

    parser_init = subparsers.add_parser("build", help="Build a sage theme on the container.")
    parser_init.add_argument("name", type=str, help="The name of the theme.")
    parser_init.set_defaults(func=build_sage_theme)

    parser_list = subparsers.add_parser("list", help="List themes installed on the container.")
    parser_list.set_defaults(func=list_themes)

    args = parser.parse_args()
    args.func(args)
