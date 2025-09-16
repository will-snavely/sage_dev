import os
import secrets
import collections
import argparse

auth_keys = [
    'AUTH_KEY',
    'SECURE_AUTH_KEY',
    'LOGGED_IN_KEY',
    'NONCE_KEY',
    'AUTH_SALT',
    'SECURE_AUTH_SALT',
    'LOGGED_IN_SALT',
    'NONCE_SALT'
] 

def get_bedrock_config():
    config = collections.OrderedDict()
    config["DB_NAME"] = os.environ["WORDPRESS_DB"]
    config["DB_USER"] = os.environ["WORDPRESS_DB_USER"]
    with open(os.environ["WORDPRESS_DB_PASSWORD_FILE"]) as f:
        config["DB_PASSWORD"] = f.read().strip()
    config["DB_HOST"] = os.environ["WORDPRESS_DB_HOST"]

    config["WP_ENV"] = "development"
    config["WP_HOME"] = os.environ["SITE_URL"]
    config["WP_SITEURL"] = "${WP_HOME}/wp"
    config["WP_DEBUG_LOG"] = "/www/srv/bedrock/debug.log"

    for key in auth_keys:
        config[key] = secrets.token_urlsafe(64)

    return config

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="The bedrock project name.")
    args = parser.parse_args()

    bedrock_env_file = f"/www/srv/bedrock/{args.name}/.env"
    if not os.path.exists(bedrock_env_file):
        with open(bedrock_env_file, "w") as f:
            config = get_bedrock_config()
            print(config)
            for k,v in config.items():
                print(k,v)
                f.write(f"{k}=\"{v}\"\n")
