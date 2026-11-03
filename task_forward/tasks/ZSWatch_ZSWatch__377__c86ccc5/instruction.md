# Recover the symbolic verification state this change produces

A regression report was filed against `ZSWatch/ZSWatch`.  The report is quoted verbatim below.

## Report

```
nrf5340dk/nfr5340/cpuapp compile error

Hello，
zswatch@5/nrf5340/cpuapp compiles successfully.

when i change board to  nrf5340dk/nfr5340/cpuapp, it fails.

The error log is as below:

In file included from E:/Projects/InnoPhase/watch/software/ZSWatch/zephyr/include/zephyr/storage/flash_map.h:277,
                 from E:/Projects/InnoPhase/watch/software/ZSWatch/app/src/filesystem/zsw_rtt_flash_loader.c:28:
E:/Projects/InnoPhase/watch/software/ZSWatch/nrf/include/flash_map_pm.h:43:22: error: 'PM_lvgl_raw_partition_ID' undeclared here (not in a function)
   43 | #define PM_ID(label) PM_##label##_ID
      |                      ^~~
E:/Projects/InnoPhase/watch/software/ZSWatch/nrf/include/flash_map_pm.h:48:35: note: in expansion of macro 'PM_ID'
   48 | #define FIXED_PARTITION_ID(label) PM_ID(label)
      |                                   ^~~~~
E:/Projects/InnoPhase/watch/software/ZSWatch/app/src/filesystem/zsw_rtt_flash_loader.c:62:6: note: in expansion of macro 'FIXED_PARTITION_ID'
   62 |     [FIXED_PARTITION_ID(lvgl_raw_partition)] = "lvgl_raw_partition",
      |      ^~~~~~~~~~~~~~~~~~
E:/Projects/InnoPhase/watch/software/ZSWatch/nrf/include/flash_map_pm.h:43:22: error: array index in initializer not of integer type
   43 | #define PM_ID(label) PM_##label##_ID
      |                      ^~~
E:/Projects/InnoPhase/watch/software/ZSWatch/nrf/include/flash_map_pm.h:48:35: note: in expansion of macro 'PM_ID'
   48 | #define FIXED_PARTITION_ID(label) PM_ID(label)
      |                                   ^~~~~
E:/Projects/InnoPhase/watch/software/ZSWatch/app/src/filesystem/zsw_rtt_flash_loader.c:62:6: note: in expansion of macro 'FIXED_PARTITION_ID'
   62 |     [FIXED_PARTITION_ID(lvgl_raw_partition)] = "lvgl_raw_partition",
      |      ^~~~~~~~~~~~~~~~~~
E:/Projects/InnoPhase/watch/software/ZSWatch/nrf/include/flash_map_pm.h:43:22: note: (near initialization for 'partition_map')
   43 | #define PM_ID(label) PM_##label##_ID
      |                      ^~~
E:/Projects/InnoPhase/watch/software/ZSWatch/nrf/include/flash_map_pm.h:48:35: note: in expansion of macro 'PM_ID'
   48 | #define FIXED_PARTITION_ID(label) PM_ID(label)
      |                                   ^~~~~
E:/Projects/InnoPhase/watch/software/ZSWatch/app/src/filesystem/zsw_rtt_flash_loader.c:62:6: note: in expansion of macro 'FIXED_PARTITION_ID'
   62 |     [FIXED_PARTITION_ID(lvgl_raw_partition)] = "lvgl_raw_partition",
      |      ^~~~~~~~~~~~~~~~~~
[806/1338] Building C object CMakeFiles/app.dir/src/filesystem/zsw_lvgl_spi_decoder.c.obj
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c86ccc5ed2af29ef08cd1eb234373360ce1d84ad`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "ZSWatch_ZSWatch__377__c86ccc5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
