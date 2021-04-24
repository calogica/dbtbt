import os
from pathlib import Path
import yaml

from dbtbt.utils.logger import logger, color_me


HEADER = """
       ____    __  __    __
  ____/ / /_  / /_/ /_  / /_
 / __  / __ \/ __/ __ \/ __/
/ /_/ / /_/ / /_/ /_/ / /_
\__,_/_.___/\__/_.___/\__/

"""


def read_yaml(yaml_path):

    try:
        with open(Path(yaml_path).resolve(), "r") as f:
            yml = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError:
        logger.info(
            color_me(
                f"Could not find '{yaml_path}'. Please check that '{yaml_path}' exists.",
                "red",
            )
        )
        raise

    return yml


def run_command(command):
    return os.system(command.strip())


def print_dry_run(args):
    if args.dry_run or args.print_dry_run:
        print_msg("Relax! It's only a dry run... 👍", "~")
    else:
        print_msg(color_me("This is *not* a test... 🚀", "red"), "~")


def print_msg(msg, sep="-"):
    lw = 100
    logger.info(f"\n{sep*lw}\n{msg}\n{sep*lw}")


def print_dbt_model_dependencies(model_list, args):
    if args.dry_run and args.print_dry_run:
        print_msg(
            f"The following models would be affected by your model selection:", "-"
        )
        dbt_ls = f"dbt ls -m {model_list}"
        rc = run_command(dbt_ls)
        return rc


def run_dbt(dbt_commands, dry_run):

    for cmd in dbt_commands:
        logger.info(cmd)
        if not dry_run:
            rc = run_command(cmd)
            if rc != 0:
                print_msg("There was an error, skipping remaining steps (if any)", "!")
                break


def check_upstream_source(args, config):

    defer_options = ""

    if args.target == "dev" and args.upstream_source == "prod":

        defer_options = "--defer --state target/prod_manifest"

        rebuild_manifest(args, config)

    return defer_options


def rebuild_manifest(args, config):

    PROD_MANIFEST_FOLDER = "target/prod_manifest"
    PROD_MANIFEST_PATH = f"{PROD_MANIFEST_FOLDER}/manifest.json"
    PROD_TARGET = config["prod"]["target"]

    if not os.path.exists(PROD_MANIFEST_PATH) or args.rebuild:

        print_msg("Rebuilding prod manifest...")

        rebuild_manifest = [
            f"mkdir -p {PROD_MANIFEST_FOLDER}",
            f"dbt compile -t {PROD_TARGET}",
            f"cp target/manifest.json {PROD_MANIFEST_PATH}",
        ]
        for cmd in rebuild_manifest:
            logger.info(cmd)
            if not args.dry_run:
                rc = run_command(cmd)
                if rc != 0:
                    break
