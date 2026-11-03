# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
[SERVICE] log_level + FLB_LOG_LEVEL env var together cause startup abort: "could not configure service property 'log_level'" (regression in 5.1.0)

## Bug Report

**Describe the bug**
If the log level is set in both places at once — the FLB_LOG_LEVEL environment variable and Log_Level in the [SERVICE] section — Fluent Bit fails to start with:

```
[error] [config] could not configure service property 'log_level'
[error] configuration file contains errors, aborting.
```

The log level is actually applied correctly (the env var overrides the config value, as intended), but flb_config_set_property() returns -1 on that path, and since 5.1.0 the caller treats that as a fatal error and aborts.

This is a regression: it works on 5.0.9 and earlier, and fails on 5.1.0 and 5.1.1.



**To Reproduce**

-both.conf:

```
[SERVICE]
    Log_Level debug
[INPUT]
    Name dummy
    Tag  test
[OUTPUT]
    Name null
    Match *

# FAILS on 5.1.0 / 5.1.1
docker run --rm -e FLB_LOG_LEVEL=debug -v "$PWD":/cfg fluent/fluent-bit:5.1.1 -c /cfg/both.conf
#   -> [error] [config] could not configure service property 'log_level' ; aborting.

# Each of these PASSES (only one source of log level):
docker run --rm                        -v "$PWD":/cfg fluent/fluent-bit:5.1.1 -c /cfg/both.conf   # config only
docker run --rm -e FLB_LOG_LEVEL=debug -v "$PWD":/cfg fluent/fluent-bit:5.1.1 -c /cfg/noconf.conf # env only (no Log_Level line)
```

**Expected behaviour**
Setting FLB_LOG_LEVEL while Log_Level is also present in [SERVICE] should start normally, with the env var taking precedence (documented behavior). No error, no abort.


Version | Result (env + config both set)
-- | --
5.0.0 | starts
5.0.9 | starts
5.1.0 | aborts
5.1.1 | aborts

**Root Cause**

In src/flb_config.c, flb_config_set_property() initializes int ret = -1; and, in the log_level branch, only assigns ret inside the if (set_log_level_from_env(config) < 0) { ... } block:
https://github.com/fluent/fluent-bit/blob/v5.1.1/src/flb_config.c#L833

```
if (!strncasecmp(key, FLB_CONF_STR_LOGLEVEL, 256)) {
    #ifndef FLB_HAVE_STATIC_CONF
    if (set_log_level_from_env(config) < 0) {   // env present -> returns 0 -> block skipped
        tmp = flb_env_var_translate(config->env, v);
        if (tmp) { ret = set_log_level(config, tmp); ... }
        else     { ret = set_log_level(config, v); }
    }
    #endif
    // when FLB_LOG_LEVEL is set, ret is never assigned -> stays -1
}
```

When FLB_LOG_LEVEL is set, set_log_level_from_env() succeeds (returns 0), so the block is skipped and ret remains -1. The function then returns -1, even though the level was set. Every other property branch (parsers_file, plugins_file, generic else) assigns ret on success; only log_level has a success path that leaves it at -1.

This bug is old and was previously harmless because the caller ignored the return value:

- 5.0.9 (return discarded): https://github.com/fluent/fluent-bit/blob/v5.0.9/src/flb_config.c#L1097

In 5.1.0 a stricter caller (set_service_property()) began checking the return value and aborting on -1, which exposed the latent bug:

- 5.1.0 caller (checked + fatal): https://github.com/fluent/fluent-bit/blob/v5.1.0/src/flb_config.c#L1543-L1551
- set_service_property() wrapper: https://github.com/fluent/fluent-bit/blob/v5.1.0/src/flb_config.c#L1455


**Proposed fix**
Record success on the env-var path by adding an else to the log_level branch:

```
                 #ifndef FLB_HAVE_STATIC_CONF
                 if (set_log_level_from_env(config) < 0) {
                     tmp = flb_env_var_translate(config->env, v);
                     if (tmp) {
                         ret = set_log_level(config, tmp);
                         flb_sds_destroy(tmp);
                         tmp = NULL;
                     }
                     else {
                         ret = set_log_level(config, v);
                     }
                 }
+                else {
+                    ret = 0;   /* env var path already applied the level successfully */
+                }
                 #endif
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4d23b1589e2d40f2225c4b84cd4b2988b962e083`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "fluent_fluent_bit__12310__4d23b15",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
