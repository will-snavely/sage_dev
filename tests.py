import argparse
import logging

from docker_util import *

logger = logging.getLogger(__name__)

def run_project_tests(args):
    project = args.project
    themes_dir = f"{BEDROCK_ROOT}/{project}/web/app/tests"
    run_docker_cmds(
        f"chmod -R g+rw {BEDROCK_ROOT}",
        f"chown -R www-data {BEDROCK_ROOT}",
        workdir=themes_dir,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    config = load_bedrock_config()
    parser.add_argument("-v", "--verbose", action="store_true")
    subparsers = parser.add_subparsers(
        title="Commands", help="Subcommand help.", required=True
    )
    parser_run = subparsers.add_parser("run")
    parser_init.set_defaults(func=run_project_tests)
    parser_init.add_argument(
        "--project",
        "-p",
        default=config.get("working_project"),
        type=str,
        help="The name of the bedrock project.",
    )

    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)
    args.func(args)
