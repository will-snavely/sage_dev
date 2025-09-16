import logging
import shlex
import subprocess

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

def run_docker_cmd(cmd, service, user=None, workdir=None):
    dcmd = docker_cmd(cmd, service=service, user=user, workdir=workdir)
    log_docker_cmd(dcmd)
    return subprocess.run(dcmd)
