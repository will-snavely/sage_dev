import argparse
import logging

from docker_util import *

logger = logging.getLogger(__name__)


def create_sage_theme(args):
    project = args.project
    theme = args.theme
    themes_dir = f"{BEDROCK_ROOT}/{project}/web/app/themes"
    run_docker_cmds(
        f"composer create-project roots/sage {theme}",
        f"chgrp -R devs {BEDROCK_ROOT}",
        f"chmod -R g+rw {BEDROCK_ROOT}",
        f"chown -R www-data {BEDROCK_ROOT}",
        workdir=themes_dir,
    )

    new_theme_dir = f"{themes_dir}/{theme}"
    search = r"\/app\/themes\/sage\/public\/build\/"
    replace = r"\/app\/themes\/" + theme + "\/public\/build\/"
    run_docker_cmd(
        f"sed -i 's/{search}/{replace}/g' vite.config.js", workdir=new_theme_dir
    )

    save_bedrock_config({"working_project": project, "working_theme": theme})


def build_sage_theme(args):
    project = args.project
    theme = args.theme
    theme_dir = f"{BEDROCK_ROOT}/{project}/web/app/themes/{theme}"
    run_docker_cmds(
        "npm install",
        "npm run build",
        f"chgrp -R devs {BEDROCK_ROOT}",
        f"chmod -R g+rw {BEDROCK_ROOT}",
        f"chown -R www-data {BEDROCK_ROOT}",
        workdir=theme_dir,
    )


def run_dev_server(args):
    project = args.project
    theme = args.theme
    theme_dir = f"{BEDROCK_ROOT}/{project}/web/app/themes/{theme}"
    run_docker_cmds(
        "npm run dev",
        user="www-data",
        workdir=theme_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    config = load_bedrock_config()

    parser.add_argument("-v", "--verbose", action="store_true")
    subparsers = parser.add_subparsers(
        title="Commands", help="Subcommand help.", required=True
    )
    parser_init = subparsers.add_parser(
        "init", help="Create a new sage theme on the container."
    )
    parser_init.set_defaults(func=create_sage_theme)
    parser_init.add_argument(
        "--project",
        "-p",
        default=config.get("working_project"),
        type=str,
        help="The name of the bedrock project.",
    )
    parser_init.add_argument("theme", type=str, help="The name of the sage theme.")

    parser_build = subparsers.add_parser("build", help="Build a sage theme")
    parser_build.set_defaults(func=build_sage_theme)
    parser_build.add_argument(
        "--project",
        "-p",
        default=config.get("working_project"),
        type=str,
        help="The name of the bedrock project.",
    )
    parser_build.add_argument(
        "--theme",
        "-t",
        default=config.get("working_theme"),
        type=str,
        help="The name of the sage theme.",
    )

    parser_run_dev = subparsers.add_parser("dev", help="Run the development server")
    parser_run_dev.set_defaults(func=run_dev_server)
    parser_run_dev.add_argument(
        "--project",
        "-p",
        default=config.get("working_project"),
        type=str,
        help="The name of the bedrock project.",
    )
    parser_run_dev.add_argument(
        "--theme",
        "-t",
        default=config.get("working_theme"),
        type=str,
        help="The name of the sage theme.",
    )

    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)
    args.func(args)
