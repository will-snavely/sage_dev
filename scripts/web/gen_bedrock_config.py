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
    wp_env = os.environ.get("WP_ENVIRON", "development")
    wp_debug = os.environ.get("WP_DEBUG", "true")
    wp_debug_display = os.environ.get("WP_DEBUG_DISPLAY", "false")
    wp_home = f"{web_protocol}://{web_hostname}"

    # Optional - application.php only turns on wp-mail-smtp's PHP-constant
    # config when SMTP_HOST is present, so these are only written to .env
    # when actually set (dev's Mailpit container, or a real provider in
    # prod), same as everywhere else in this project that leaves SMTP
    # unconfigured by default.
    #
    # Read from WORDPRESS_SMTP_* (not SMTP_*) deliberately, same reasoning as
    # WORDPRESS_DB_HOST vs DB_HOST below: if the container's raw environment
    # already has a var named exactly SMTP_HOST, phpdotenv's immutable .env
    # loading in application.php sees it as "already set" (via getenv()) and
    # skips populating $_ENV for it - and env() there reads $_ENV, not
    # getenv(), so it would never see the value. Using a differently-named
    # source var avoids that collision entirely. Used identically in both
    # dev (Mailpit, no auth needed) and prod (a real provider, credentials
    # required) - only the values differ.
    smtp_host = os.environ.get("WORDPRESS_SMTP_HOST")
    smtp_port = os.environ.get("WORDPRESS_SMTP_PORT")
    smtp_encryption = os.environ.get("WORDPRESS_SMTP_ENCRYPTION")
    smtp_user = os.environ.get("WORDPRESS_SMTP_USER")
    smtp_pass_file = os.environ.get("WORDPRESS_SMTP_PASS_FILE")
    smtp_from_email = os.environ.get("WORDPRESS_SMTP_FROM_EMAIL")
    smtp_from_name = os.environ.get("WORDPRESS_SMTP_FROM_NAME")

    config["DB_NAME"] = db_name
    config["DB_USER"] = db_user
    with open(db_password_file) as f:
        config["DB_PASSWORD"] = f.read().strip()
    config["DB_HOST"] = db_host

    config["WP_ENV"] = wp_env
    config["WP_DEBUG"] = wp_debug
    config["WP_DEBUG_DISPLAY"] = wp_debug_display
    config["WP_HOME"] = wp_home
    config["WP_SITEURL"] = f"{wp_home}/wp"
    config["WP_DEBUG_LOG"] = f"{bedrock_root}/{project_name}/web/app/debug.log"

    if smtp_host:
        config["SMTP_HOST"] = smtp_host
        if smtp_port:
            config["SMTP_PORT"] = smtp_port
        if smtp_encryption:
            config["SMTP_ENCRYPTION"] = smtp_encryption
        if smtp_user:
            config["SMTP_USER"] = smtp_user
        if smtp_pass_file:
            with open(smtp_pass_file) as f:
                config["SMTP_PASS"] = f.read().strip()
        if smtp_from_email:
            config["SMTP_FROM_EMAIL"] = smtp_from_email
        if smtp_from_name:
            config["SMTP_FROM_NAME"] = smtp_from_name

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
