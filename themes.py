import argparse
import subprocess
import collections
import os
import sys
import json

def push_theme(args):
    pass

def pull_theme(args):
    pass

def list_themes(args):
    command = [
        "docker-compose", "exec",
        "--workdir", "/srv/www/wordpress",
        "--user", "www-data",
        "web",
        "wp", "theme", "list"]
    print(" ".join(command))
    result = subprocess.run(command)

def create_sage_theme(args):
    cwd = os.getcwd()
    name = args.name
    host_theme_dir = os.path.join(cwd, "themes", name)
    web_themes_dir = "/srv/www/wordpress/wp-content/themes"
    os.makedirs(host_theme_dir, exist_ok=True)

    command = [
        "docker-compose", "exec",
        "--workdir", web_themes_dir,
        "web",
        "composer", "create-project", "roots/sage", name]
    result = subprocess.run(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="Commands", help='Subcommand help.')
    parser_init = subparsers.add_parser("init", help="Create a new sage theme on the container.")
    init_subparsers = parser_init.add_subparsers(title="Builder", help='Select a theme builder.')
    parser_sage_init = init_subparsers.add_parser("sage", help="Create a blank Sage theme.")
    parser_sage_init.add_argument("name", type=str, help="The name of the theme.")
    parser_sage_init.set_defaults(func=create_sage_theme)

    parser_pull = subparsers.add_parser("pull", help="Pull a theme from the container.")
    parser_pull.add_argument("name", type=str, help="The name of the theme.")
    parser_pull.set_defaults(func=pull_theme)

    parser_push = subparsers.add_parser("push", help="Push a theme from the container.")
    parser_push.add_argument("name", type=str, help="The name of the theme.")
    parser_push.set_defaults(func=push_theme)

    parser_push = subparsers.add_parser("list", help="List themes installed on the container.")
    parser_push.set_defaults(func=list_themes)

    args = parser.parse_args()
    args.func(args)
