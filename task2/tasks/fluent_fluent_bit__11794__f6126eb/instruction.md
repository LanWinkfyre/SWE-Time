# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
out_file: Enabled record accessor for path and file configuration parameters

**Describe the solution you'd like**
Being able to dynamically create files according to some field in the log record would be very appreciated. For instance, when reading logs from Proxies it would be nice to store the logs in a file that would correspond to, for instance, the host of the request. The same would be for the `path` configuration parameter, for instance, we have multiple proxies and we want to create directories and store the records based on the proxy name which is inside the log record. 

Accessing data from the Logs already happens in other plugins like `rewrite_tag` (See example bellow), and `out_opensearch` where you can define the `index_name` with data from the log itself, so this would be just a matter of having a bit more consistency rather than a completely new feature.

**Describe alternatives you've considered**
There is a current work around for the file parameter but it's ugly and tricky, which is to rewrite the TAG of the record to whatever we want. Later on, the `out_file` will name the file according to the TAG name if no `File` parameter was provided.

**Additional context**
Let's give an example:

I want to write my logs into a directory based on the `proxy_name` field and a file based on the `hostname` field of my logs. My proxies are: `proxy1` & `proxy2`. My hosts are: `host1` & `host2`.

***Current work around solution***
```
[INPUT]
    Name      forward
    Tag           proxy-requests
    Listen       0.0.0.0
    Port          24224

[FILTER]
    Name    rewrite_tag
    Match   proxy-requests

    Rule    $proxy_name ^(.*)$ $proxy_name.$hostname.log false

[OUTPUT]
    Match       proxy1*
    Name        file
    path        /proxy1/
    Format      plain

[OUTPUT]
    Match       proxy2*
    Name        file
    path        /proxy2/
    Format      plain
```

The above extended and ugly configuration will generate the following files which are not the best naming but work:

/proxy1/proxy1.host1.log
/proxy1/proxy1.host2.log
/proxy2/proxy2.host1.log
/proxy2/proxy2.host2.log

***Desired***
```
[INPUT]
    Name      forward
    Tag           proxy-requests
    Listen       0.0.0.0
    Port          24224

[OUTPUT]
    Match       *
    Name        file
    Path          /$proxy_name/
    File            $hostname.log
    Format      plain

```
The above simpler config would generate the desired behavior:

/proxy1/host1.log
/proxy1/host2.log
/proxy2/host1.log
/proxy2/host2.log

**Edge cases & considerations**
***Missing field***
If there referenced field doesn't exist, you could make it configurable like `On_Missing_Field drop|fallback|use_default` or just apply as default one of the following `drop`, `fallback` `use_default`

***Data Validation***
Data coming from the record should be validated to comply with filesystem naming standard, but I believe this could be something do use should be careful about. And a simple notice on the documentation would help.

***High cardinality / file descriptor exhaustion***
This again should be something the user needs to be careful about, or a new configuration field like `max-open-files` could be introduced. And again, a little notice on the documentation about this would work as well.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f6126ebc3aba26882e8e1f2c20e93f04f6d7489c`.  There
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
{"case_id": "fluent_fluent_bit__11794__f6126eb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
