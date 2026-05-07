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


def get_bedrock_config(project_name):
    config = collections.OrderedDict()
    bedrock_root = os.environ.get("BEDROCK_ROOT")

    db_host = os.environ.get("WORDPRESS_DB_HOST")
    db_name = os.environ.get("WORDPRESS_DB")
    db_user = os.environ.get("WORDPRESS_DB_USER")
    db_password_file = os.environ.get("WORDPRESS_DB_PASSWORD_FILE")
    web_protocol = os.environ.get("WEB_PROTOCOL", "http")
    web_hostname = os.environ.get("WEB_HOSTNAME", "web")
    wp_env = os.environ.get("WP_ENV", "development")
    wp_debug = os.environ.get("WP_DEBUG", "true")
    wp_debug_display = os.environ.get("WP_DEBUG_DISPLAY", "false") 

    config["DB_NAME"] = db_name
    config["DB_USER"] = db_user
    with open(db_password_file) as f:
        config["DB_PASSWORD"] = f.read().strip()
    config["DB_HOST"] = db_host

    config["WP_ENV"] = wp_env
    config["WP_DEBUG"] = wp_debug
    config["WP_DEBUG_DISPLAY"] = wp_debug_display
    config["WP_SITEURL"] = "${WP_HOME}/wp"
    config["WP_HOME"] = f"{web_protocol}://{web_hostname}"
    config["WP_DEBUG_LOG"] = f"{bedrock_root}/{project_name}/web/app/debug.log"

    for key in auth_keys:
        config[key] = secrets.token_urlsafe(64)

    return config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="The bedrock project name.")
    args = parser.parse_args()

    project_name = args.name
    bedrock_root = os.environ["BEDROCK_ROOT"]
    bedrock_env_file = f"{bedrock_root}/{args.name}/.env"
    extra_config_file = f"{bedrock_root}/{args.name}/.env.extra"
    extra_config = ""

    if os.path.exists(extra_config_file):
        with open(extra_config_file) as f:
            extra_config = f.read()
    with open(bedrock_env_file, "w") as f:
        config = get_bedrock_config(project_name)
        for k, v in config.items():
            if str(v).lower() in ("true", "false"):
                f.write(f'{k}={str(v).lower()}\n')
            elif isinstance(v, (int, float)):
                f.write(f'{k}={v}\n')
            else:
                f.write(f'{k}="{v}"\n')
        f.write(extra_config)
