import os
import secrets
import collections
import argparse

auth_keys = [
    "AUTH_KEY",
    "SECURE_AUTH_KEY",
    "LOGGED_IN_KEY",
    "NONCE_KEY",
    "AUTH_SALT",
    "SECURE_AUTH_SALT",
    "LOGGED_IN_SALT",
    "NONCE_SALT",
]


def get_bedrock_config(
    db_host,
    db_name,
    db_user,
    db_password_file,
    web_hostname,
    web_port,
):
    config = collections.OrderedDict()
    config["DB_NAME"] = db_name
    config["DB_USER"] = db_user
    with open(db_password_file) as f:
        config["DB_PASSWORD"] = f.read().strip()
    config["DB_HOST"] = db_host

    config["WP_ENV"] = "development"
    config["WP_HOME"] = f"http://{web_hostname}"
    config["WP_SITEURL"] = "${WP_HOME}/wp"
    config["WP_DEBUG_LOG"] = f"debug.log"

    for key in auth_keys:
        config[key] = secrets.token_urlsafe(64)

    return config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="The bedrock project name.")
    args = parser.parse_args()

    bedrock_root = os.environ["BEDROCK_ROOT"]
    bedrock_env_file = f"{bedrock_root}/{args.name}/.env"
    extra_config_file = f"{bedrock_root}/{args.name}/.env.extra"
    extra_config = ""
    if os.path.exists(extra_config_file):
        with open(extra_config_file) as f:
            extra_config = f.read()
    with open(bedrock_env_file, "w") as f:
        config = get_bedrock_config(
            os.environ["WORDPRESS_DB_HOST"],
            os.environ["WORDPRESS_DB"], 
            os.environ["WORDPRESS_DB_USER"], 
            os.environ["WORDPRESS_DB_PASSWORD_FILE"],
            os.environ["WEB_HOSTNAME"],
            os.environ["WEB_PORT"]
        )
        for k, v in config.items():
            f.write(f'{k}="{v}"\n')
        f.write(extra_config)
