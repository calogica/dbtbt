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

1. Run a full refresh of models in `dev`
2. (Optional) Run models incrementally in `dev`
3. Run tests in `dev`


### Usage:
```
usage: dbtbt build [-h] -m MODELS [MODELS ...] [-e EXCLUDE [EXCLUDE ...]]
                   [-t {dev,prod}] [-r] [-i] [-d] [-p] [-u {dev,prod}]

optional arguments:
  -h, --help            show this help message and exit
  -m MODELS [MODELS ...], --models MODELS [MODELS ...]
                        List of models to run, e.g. date_d device_model_d
  -e EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        List of models to exclude, e.g. date_d device_model_d
  -t {dev,prod}, --target {dev,prod}
                        Name of dbt target as specified in profiles.yml. If
                        left blank, default target (dev) will be used
  -r, --rebuild         If set, will rebuild prod manifest
  -i, --incremental     If set, will also run models incrementally
  -d, --dry-run         If set, will print commands to screen only
  -p, --print-dry-run   If set, will print commands to screen only including
                        the models affected by --models
  -u {dev,prod}, --upstream-source {dev,prod}
                        If set to 'prod', will use prod manifest to build
                        unselect upstream models. When target is 'dev', 'prod'
                        is the default upstream source.
```

*Note*: since this is a dev only tool, it ignores the `-t`/`--target` command line flag

### Examples

Let's build a new model called `fct_my_model`, which is a large XA model selecting from a large fact table, `playback_session_f`.

---

Build `playback_session_xa` in `dev` using data in the `dev` project only

[**dev.playback_session_xa**]

```
python build_me.py --models playback_session_xa
```

---

Build `playback_session_xa` and all of its upstream dependencies in `dev` using data in the `dev` project only

[**++dev.playback_session_f** --> **dev.playback_session_xa**]

```
python build_me.py --models +playback_session_xa
```

---

Build `playback_session_xa` and all of its upstream dependencies in `dev` using data in the `dev` project only but only print the commands that would be run, including a list of models affected by the model selector:

[**++dev.playback_session_f** --> **dev.playback_session_xa**]

```
python build_me.py --models +playback_session_xa --dry-run
```

---

Build `playback_session_xa` and all of its upstream dependencies in `dev` using data in the `dev` project only but only print the commands that would be run, including a list of models affected by the model selector:

[**++dev.playback_session_f** --> **dev.playback_session_xa**]

```
python build_me.py --models +playback_session_xa --print-dry-run
```
This will use `dbt ls` to list the affected models:
```
----------------------------------------------------------------------------------------------------
The following models would be affected by your model selection:
----------------------------------------------------------------------------------------------------
quibi_analytics._transform.account._accounts_first_country
quibi_analytics.dw.account.account_d
quibi_analytics.dw.account.account_day_r
quibi_analytics.dw.content.episode_age_r
quibi_analytics.dw.playback.playback_session_f
quibi_analytics.xa.playback_session_xa
quibi_analytics.dw.content.season_age_r
quibi_analytics.dw.content.show_d
...
```

---

Build `playback_session_xa` in `dev` using upstream data from the `prod` project. Note that we are not rebuilding the upstream dependencies, we're simply reading from their `prod` versions.

[*prod.playback_session_f* --> **dev.playback_session_xa**]

```
python build_me.py --models playback_session_xa --upstream-source prod
```

---

Build `playback_session_xa` in `dev` using upstream data from the `prod` project and include an `incremental` run as well to test incremental load logic.

[*prod.playback_session_f* --> **dev.playback_session_xa**]

```
python build_me.py --models playback_session_xa --upstream-source prod --incremental
```

---

Build `playback_session_f` and `playback_session_xa` in `dev` using upstream data from the `prod` project. So, both of these models will be built in `dev`, but `playback_session_xa` will read from `playback_session_f` in `dev` since it's part of the model selection. However, any upstream sources for `playback_session_f` will come from `prod`.

[*prod.tf_playback_session_episode_metrics* --> **dev.playback_session_f** --> **dev.playback_session_xa**]

```
python build_me.py --models playback_session_f playback_session_xa --upstream-source prod
```

## dbtbt deploy

Use this to deploy models that have recently been merged to `main` via pull request and need to deployed to `quibidw` - either because the structure of the model changed (add/remove columns) or because business logic changed requiring us to rebuild the table in production.

The `deploy_me.py` differs from `build_me.py` in that it first builds models in `<target>_audit`, then tests in `<target>_audit` before publishing to `<target>`.

It runs the following steps:

1. Update dbt dependencies
2. Run a full refresh of models in `<target>_audit`
3. (Optional) Run models incrementally in `<target>_audit`
4. Run tests in `<target>_audit`
5. Run a full refresh of models in `<target>`, excluding any models in `_transform` folder

Usage:

```
usage: deploy_me.py [-h] -m MODELS [MODELS ...] [-e EXCLUDE [EXCLUDE ...]]
                   [-t {dev,prod}] [-r] [-i] [-d] [-p] [-u {dev,prod}]

optional arguments:
  -h, --help            show this help message and exit
  -m MODELS [MODELS ...], --models MODELS [MODELS ...]
                        List of models to run, e.g. date_d device_model_d
  -e EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        List of models to exclude, e.g. date_d device_model_d
  -t {dev,prod}, --target {dev,prod}
                        Name of dbt target as specified in profiles.yml. If
                        left blank, default target (dev) will be used
  -r, --rebuild         If set, will rebuild prod manifest
  -i, --incremental     If set, will also run models incrementally
  -d, --dry-run         If set, will print commands to screen only
  -p, --print-dry-run   If set, will print commands to screen only including
                        the models affected by --models
  -u {dev,prod}, --upstream-source {dev,prod}
                        If set to 'prod', will use prod manifest to build
                        unselect upstream models. When target is 'dev', 'prod'
                        is the default upstream source.
```

### Examples

Let's deploy a new model called `playback_session_xa`, which is a large XA model selecting from a large fact table, `playback_session_f`.

---

Deploy `playback_session_xa` to `prod`

[**prod.playback_session_xa**]

```
python deploy_me.py --models playback_session_xa --target prod
```

---

Deploy `playback_session_xa` to `prod` but only print the commands that would be run

[**prod.playback_session_xa**]

```
python deploy_me.py --models playback_session_xa --target prod --dry-run
```

---

Deploy `playback_session_xa` to `prod` but only print the commands that would be run, including a list of models affected by the model selector

[**prod.playback_session_xa**]

```
python deploy_me.py --models playback_session_xa --target prod --dry-run
```

This will use `dbt ls` to list the affected models:
```
----------------------------------------------------------------------------------------------------
The following models would be affected by your model selection:
----------------------------------------------------------------------------------------------------
quibi_analytics._transform.account._accounts_first_country
quibi_analytics.dw.account.account_d
quibi_analytics.dw.account.account_day_r
quibi_analytics.dw.content.episode_age_r
quibi_analytics.dw.playback.playback_session_f
quibi_analytics.xa.playback_session_xa
quibi_analytics.dw.content.season_age_r
quibi_analytics.dw.content.show_d
...
```

---

Deploy `playback_session_xa` and all of its downstream dependencies to `prod`

[**++dev.playback_session_f** --> **dev.playback_session_xa**]

```
python deploy_me.py --models playback_session_xa+ --target prod
```

---

Deploy `playback_session_f` and `playback_session_xa` in `dev` using upstream data from the `prod` project. This is useful to test a deploy before deploying to `prod`.

[*prod.tf_playback_session_episode_metrics* --> **dev.playback_session_f** --> **dev.playback_session_xa**]

```
python deploy_me.py --models playback_session_f playback_session_xa --upstream-source prod
```
