from dbtbt.utils.utils import (
    HEADER,
    print_dry_run,
    print_dbt_model_dependencies,
    print_msg,
    check_upstream_source,
    run_dbt,
)


class Build(object):
    """
    Build class
    """

    @staticmethod
    def build(args, config, model_list, exclude_list):

        TARGET = config[args.target]["target"]

        args.upstream_source = (
            "dev" if not args.upstream_source else args.upstream_source
        )

        print_dry_run(args)
        print_dbt_model_dependencies(model_list, args)

        upstream_source = check_upstream_source(args)

        print_msg(f"Building model(s): {model_list}")
        exclude_statement = f"--exclude {exclude_list}" if len(exclude_list) > 0 else ""
        dbt_full_refresh = f"dbt run -m {model_list} {exclude_statement} --fail-fast --target {TARGET} --full-refresh {upstream_source}"
        dbt_incremental = f"dbt run -m {model_list} {exclude_statement} --fail-fast {upstream_source} --target {TARGET}"
        dbt_test = f"dbt test -m {model_list} --target {TARGET}"

        dbt_commands = []
        dbt_commands.append(dbt_full_refresh)

        if args.incremental:
            dbt_commands.append(dbt_incremental)

        dbt_commands.append(dbt_test)

        run_dbt(dbt_commands, args.dry_run)
