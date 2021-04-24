import argparse

from dbtbt.utils.utils import (
    read_yaml,
    HEADER)
from dbtbt.build import Build
from dbtbt.deploy import Deploy

from dbtbt.utils.logger import logger, color_me


def get_parsed_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("action", type=str, choices=["build", "deploy"], default="build", help="'build' or 'deploy'")
    parser.add_argument("-m", "--models", nargs='+', required=True, help="List of models to run, e.g. dim_my_dim_table fct_my_fact_table")
    parser.add_argument("-e", "--exclude", nargs='+', help="List of models to exclude, e.g. dim_my_dim_table fct_my_fact_table")
    parser.add_argument("-t", "--target",
                        type=str,
                        choices=["dev", "prod"],
                        default="dev",
                        help="Name of dbt target as specified in profiles.yml. If left blank, default target (dev) will be used")
    parser.add_argument("-w", "--wap", action="store_true", help="If set, will deploy using Write-Audit-Publish approach, requires a `*_audit` target")
    parser.add_argument("-r", "--rebuild", action="store_true", help="If set, will rebuild prod manifest")
    parser.add_argument("-i", "--incremental", action="store_true", help="If set, will also run models incrementally")
    parser.add_argument("-d", "--dry-run", action="store_true", help="If set, will print commands to screen only")
    parser.add_argument("-p", "--print-dry-run", action="store_true", help="If set, will print commands to screen only including the models affected by --models")
    parser.add_argument("-u", "--upstream-source",
                        type=str,
                        choices=["dev", "prod"],
                        help="If set to 'prod', will use prod manifest to build unselect upstream models. When target is 'dev', 'prod' is the default upstream source.")

    parser.add_argument("-c", "--config_file", type=str, default="dbtbt-config.yml")

    args = parser.parse_args()
    if args.print_dry_run:
        args.dry_run = True

    model_list = f"{' '.join(args.models)}"
    exclude_list = f"{' '.join(args.exclude)}" if args.exclude else ""

    return args, model_list, exclude_list


def main():

    logger.info(color_me(HEADER, "green"))

    args, model_list, exclude_list = get_parsed_args()

    actions = ["build", "deploy"]

    assert (
        args.action in actions
    ), f"'{args.action}' is currently not supported"

    config = read_yaml(args.config_file)

    assert (
        "dev" in config and "prod" in config
    ), "'dev' and 'prod' target names need to be specified in config.yml"

    if args.action == "build":
        Build.build(args, config, model_list, exclude_list)

    elif args.action == "deploy":
        Deploy.deploy(args, config, model_list, exclude_list)

if __name__ == "__main__":
   main()
