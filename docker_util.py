import logging
import shlex
import subprocess
import json

logger = logging.getLogger(__name__)
BEDROCK_CONF = ".bedrock.conf"
BEDROCK_ROOT = "/www/srv/projects"


def load_bedrock_config(src=BEDROCK_CONF):
    try:
        with open(src) as f:
            return json.load(f)
    except:
        return {}


def save_bedrock_config(config, dest=BEDROCK_CONF):
    with open(dest, "w") as f:
        json.dump(config, f, indent=4)


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


def run_docker_cmd(cmd, service="dev", user=None, workdir=None):
    dcmd = docker_cmd(cmd, service=service, user=user, workdir=workdir)
    log_docker_cmd(dcmd)
    return subprocess.run(dcmd)


def run_docker_cmds(*cmds, service="dev", user=None, workdir=None):
    for cmd in cmds:
        run_docker_cmd(cmd, service, user=user, workdir=workdir)
