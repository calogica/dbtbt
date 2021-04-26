```
       ____    __  __    __
  ____/ / /_  / /_/ /_  / /_
 / __  / __ \/ __/ __ \/ __/
/ /_/ / /_/ / /_/ /_/ / /_
\__,_/_.___/\__/_.___/\__/

```

# 🚀 dbt build tools

`dbtbt` is a collection of developer tools to make building (run & test) and deploying models easier.

## dbtbt build

Use this to `run` and `test` your dbt models in your `dev` project.

It runs the following steps:

1. Run a full refresh of models in `{target}`
2. (Optionally) Run models incrementally in `{target}`
3. Run tests in `{target}`

### Install

This package is not yet on PyPI and needs to be installed locally as a dev package.

1. Clone the Github repo:
`git clone git@github.com:calogica/dbtbt.git`

2. Create a new Python `venv`

3. Navigate to the repo folder and install as a local dev package.
`pip install -e .`

You should then be able to call `dbtbt` from anywhere in the Python `venv` created earlier. Note that `dbt` also needs to be installed in this `venv`.
### Usage

```zsh
usage: dbtbt build [-h] -m MODELS [MODELS ...]
    [-e EXCLUDE [EXCLUDE ...]] [-t {dev,prod}]
    [-w] [-r] [-i] [-d] [-p]
    [-u {dev,prod}] [-c CONFIG_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -m MODELS [MODELS ...], --models MODELS [MODELS ...]
                        List of models to run, e.g. dim_my_dim_table fct_my_fact_table
  -e EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        List of models to exclude, e.g. dim_my_dim_table fct_my_fact_table
  -t {dev,prod}, --target {dev,prod}
                        Name of dbt target as specified in profiles.yml. If left blank, default
                        target (dev) will be used
  -w, --wap             If set, will deploy using Write-Audit-Publish approach, requires a
                        `*_audit` target
  -r, --rebuild         If set, will rebuild prod manifest
  -i, --incremental     If set, will also run models incrementally
  -d, --dry-run         If set, will print commands to screen only
  -p, --print-dry-run   If set, will print commands to screen only including the models affected
                        by --models
  -u {dev,prod}, --upstream-source {dev,prod}
                        If set to 'prod', will use prod manifest to build unselect upstream
                        models. When target is 'dev', 'prod' is the default upstream source.
  -c CONFIG_FILE, --config_file CONFIG_FILE
```

### Examples

Let's build a new model called `fct_my_model`, which is a large fact model selecting from a large source table, `stg_my_staging_model`.

---

Build `fct_my_model` in `dev` using data in the `dev` project only

[**dev.fct_my_model**]

```zsh
dbtbt build --models fct_my_model
```

---

Build `fct_my_model` and all of its upstream dependencies in `dev` using data in the `dev` project only

[**++dev.stg_my_staging_model** --> **dev.fct_my_model**]

```zsh
dbtbt build --models +fct_my_model
```

---

Build `fct_my_model` and all of its upstream dependencies in `dev` using data in the `dev` project only but only print the commands that would be run, including a list of models affected by the model selector:

[**++dev.stg_my_staging_model** --> **dev.fct_my_model**]

```zsh
dbtbt build --models +fct_my_model --dry-run
```

---

Build `fct_my_model` and all of its upstream dependencies in `dev` using data in the `dev` project only but only print the commands that would be run, including a list of models affected by the model selector:

[**++dev.stg_my_staging_model** --> **dev.fct_my_model**]

```zsh
dbtbt build --models +fct_my_model --print-dry-run
```

This will use `dbt ls` to list the affected models:

```zsh
---------------------------------------------------------------------------------------------------
The following models would be affected by your model selection:
----------------------------------------------------------------------------------------------------
my_project.stg.stg_my_other_staging_model
my_project.stg.stg_my_staging_model
my_project.dw.fct_my_model
...
```

---

Build `fct_my_model` in `dev` using upstream data from the `prod` database. Note that we are not rebuilding the upstream dependencies, we're simply reading from their `prod` versions, unless they exist in `dev` (Note: this is new in dbt 0.19+).

[*prod.stg_my_staging_model* --> **dev.fct_my_model**]

```zsh
dbtbt build --models fct_my_model --upstream-source prod
```

---

Build `fct_my_model` in `dev` using upstream data from the `prod` database and include an `incremental` run as well to test incremental load logic.

[*prod.stg_my_staging_model* --> **dev.fct_my_model**]

```zsh
dbtbt build --models fct_my_model --upstream-source prod --incremental
```

---

Build `stg_my_staging_model` and `fct_my_model` in `dev` using upstream data from the `prod` database. So, both of these models will be built in `dev`, but `fct_my_model` will read from `stg_my_staging_model` in `dev` since it's part of the model selection. However, any upstream sources for `stg_my_staging_model` will come from `prod` if it does not exist in `dev`.

[*prod.stg_my_other_staging_model* --> **dev.stg_my_staging_model** --> **dev.fct_my_model**]

```zsh
dbtbt build --models stg_my_staging_model fct_my_model --upstream-source prod
```

## dbtbt deploy

Use this to deploy models that have recently been merged to `main` via pull request and need to deployed to your production environment - either because the structure of the model changed (add/remove columns) or because business logic changed requiring us to rebuild the table in production.

It runs the following steps:

1. Update dbt dependencies
2. (Optionally) Run a full refresh of models in `{audit_target}`
3. (Optionally) Run models incrementally in `{audit_target}`
4. (Optionally) Run tests in `{audit_target}`
5. Run a full refresh of models in `{target}`, excluding any models defined in `{wap:exclude}`

Usage:

```zsh
usage: dbtbt deploy [-h] -m MODELS [MODELS ...]
        [-e EXCLUDE [EXCLUDE ...]] [-t {dev,prod}]
        [-w] [-r] [-i] [-d] [-p]
        [-u {dev,prod}] [-c CONFIG_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -m MODELS [MODELS ...], --models MODELS [MODELS ...]
                        List of models to run, e.g. dim_my_dim_table fct_my_fact_table
  -e EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        List of models to exclude, e.g. dim_my_dim_table fct_my_fact_table
  -t {dev,prod}, --target {dev,prod}
                        Name of dbt target as specified in profiles.yml. If left blank, default target (dev) will be used
  -w, --wap             If set, will deploy using Write-Audit-Publish approach, requires a `*_audit` target
  -r, --rebuild         If set, will rebuild prod manifest
  -i, --incremental     If set, will also run models incrementally
  -d, --dry-run         If set, will print commands to screen only
  -p, --print-dry-run   If set, will print commands to screen only including the models affected by --models
  -u {dev,prod}, --upstream-source {dev,prod}
                        If set to 'prod', will use prod manifest to build unselect upstream models. When target is 'dev', 'prod' is the default
                        upstream source.
  -c CONFIG_FILE, --config_file CONFIG_FILE

```

### Examples

Let's deploy a new model called `fct_my_model`, which is a large XA model selecting from a large fact table, `stg_my_staging_model`.

---

Deploy `fct_my_model` to `prod`

[**prod.fct_my_model**]

```
dbtbt deploy --models fct_my_model --target prod
```

---

Deploy `fct_my_model` to `prod` but only print the commands that would be run

[**prod.fct_my_model**]

```zsh
dbtbt deploy --models fct_my_model --target prod --dry-run
```

---

Deploy `fct_my_model` to `prod` but only print the commands that would be run, including a list of models affected by the model selector

[**prod.fct_my_model**]

```zsh
dbtbt deploy --models fct_my_model --target prod --dry-run
```

This will use `dbt ls` to list the affected models:

```zsh
----------------------------------------------------------------------------------------------------
The following models would be affected by your model selection:
----------------------------------------------------------------------------------------------------
my_project.stg.stg_my_other_staging_model
my_project.stg.stg_my_staging_model
my_project.dw.fct_my_model
...
```

---

Deploy `fct_my_model` and all of its downstream dependencies to `prod`

[**++dev.stg_my_staging_model** --> **dev.fct_my_model**]

```zsh
dbtbt deploy --models fct_my_model+ --target prod
```

---

Deploy `stg_my_staging_model` and `fct_my_model` in `dev` using upstream data from the `prod` database. This is useful to test a deploy before deploying to `prod`.

[*prod.stg_my_other_staging_model* --> **dev.stg_my_staging_model** --> **dev.fct_my_model**]

```zsh
dbtbt deploy --models stg_my_staging_model fct_my_model --upstream-source prod
```
