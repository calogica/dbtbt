import sys

from dbtbt.utils.utils import (
    HEADER,
    print_dry_run,
    print_dbt_model_dependencies,
    print_msg,
    run_command,
    check_upstream_source,
    run_dbt,
)

from dbtbt.utils.logger import logger

PROD_WARNING = """
!!!!!!**** WARNING YOU ARE ABOUT TO WRITE TO PROD. ****!!!!!!\n
Type PROD to confirm you would like to do this:\n
"""


class Deploy(object):
    """
    Build class
    """

    @staticmethod
    def deploy(args, config, model_list, exclude_list):

        TARGET = config[args.target]["target"]
        if args.wap:
            assert (
                "audit_target" in config[args.target]
            ), "'audit_target' needs to be specified in config.yml in order to deploy models using Write-Audit-Publish (WAP)"

            AUDIT_TARGET = config[args.target]["audit_target"]
            POST_AUDIT_EXCLUDE = config["wap"]["exclude"]

        args.upstream_source = (
            "prod" if not args.upstream_source else args.upstream_source
        )

        if args.target == "prod" and not args.dry_run:

            prod_confirmation = input(PROD_WARNING)

            if prod_confirmation != "PROD":
                logger.info("\nGoodbye!")
                sys.exit()

        print_dry_run(args)
        print_dbt_model_dependencies(model_list, args)

        upstream_source = check_upstream_source(args, config)

        print_msg(f"Deploying model(s): {model_list}")

        exclude_statement = (
            f" --exclude {exclude_list}" if len(exclude_list) > 0 else ""
        )

        dbt_deps = "dbt deps"
        fail_fast = " --fail-fast" if config["fail_fast"] else ""

        if args.wap:
            dbt_audit_full_refresh = f"dbt run -m {model_list}{exclude_statement}{fail_fast}{upstream_source} --target {AUDIT_TARGET} --full-refresh"
            dbt_audit_incremental = f"dbt run -m {model_list}{exclude_statement}{fail_fast}{upstream_source} --target {AUDIT_TARGET}"
            dbt_audit_test = f"dbt test -m {model_list}{exclude_statement}{upstream_source} --target {AUDIT_TARGET}"

            if POST_AUDIT_EXCLUDE:
                exclude_list = f"{exclude_list} {POST_AUDIT_EXCLUDE}".strip()

        post_exclude_statement = (
            f" --exclude {exclude_list}" if len(exclude_list) > 0 else ""
        )
        dbt_full_refresh = f"dbt run -m {model_list}{post_exclude_statement}{fail_fast}{upstream_source} --target {TARGET} --full-refresh"
        dbt_test = f"dbt test -m {model_list}{post_exclude_statement}{upstream_source} --target {TARGET}"

        dbt_commands = []

        if config["refresh_deps"]:
            dbt_commands.append(dbt_deps)

        if args.wap:
            dbt_commands.append(dbt_audit_full_refresh)

            if args.incremental:
                dbt_commands.append(dbt_audit_incremental)

            dbt_commands.append(dbt_audit_test)

        dbt_commands.append(dbt_full_refresh)
        dbt_commands.append(dbt_test)

        run_dbt(dbt_commands, args.dry_run)
