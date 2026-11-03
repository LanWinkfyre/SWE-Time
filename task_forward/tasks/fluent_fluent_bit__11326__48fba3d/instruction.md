# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Using grep filter as conditional log processor ignores any condition clauses

## Bug Report

Setup using a grep filter as a log processor and give it a condition. Seems the condition is completely ignored - there are no obvious errors but fluent-bit gives the output as if it is not there.

**To Reproduce**

Run with the following configuration file (adapted from some of the documentation examples):

```
pipeline:
  inputs:
    - name: dummy
      dummy: '{"endpoint":"localhost", "value":"something"},
              {"endpoint":"localhost2", "value":"something"},
              {"endpoint":"farhost", "value":"nothing"}'
      tag: dummy
      processors:
        logs:
          - name: grep
            logical_op: and
            regex:
              - value something
            condition:
              op: and
              rules:
                - field: "$endpoint"
                  op: eq
                  value: "localhost2"

  outputs:
    - name: stdout
      match: '*'
```

OK this is not explicitly documented behaviour, but I would expect it to behave so that: if the condition
matched (endpoiint==localhost2) then the grep operated so value needs to equal something, otherwise
the grep to be ignored. Thus I would expect matches on all lines but for different reasons. What I
actually see are lines like:

```
[0] dummy: [[1767349589.147330566, {}], {"endpoint"=>"localhost", "value"=>"something"}]
[1] dummy: [[1767349589.147330566, {}], {"endpoint"=>"localhost2", "value"=>"something"}]
[0] dummy: [[1767349590.147556274, {}], {"endpoint"=>"localhost", "value"=>"something"}]
[1] dummy: [[1767349590.147556274, {}], {"endpoint"=>"localhost2", "value"=>"som
```

It is matching the first two lines where the value is "something" and seemingly ignoring endpoint.

**Your Environment**
<!--- Include as many relevant details about the environment you experienced the bug in -->

- Version: 4.2.0
- I am actually running "docker run --rm -v .:/fluent-bit/etc-extra fluent/fluent-bit:4.2.0-amd64 --config=/fluent-bit/etc-extra/grep-processor-with-cond.yaml" where grep-processor-with-cond.yaml is the config file above.

**Additional context**

What I am actually trying to do is to reduce the size of the logs we generate because for some generated
logs (I can tell these from a regular expression on one of the fields - let's say "foo .*bar.*) but we always
to keep summary fields even in this category (again we can tell from another field, say "hum .*bug.*).
Effectively we want to keep the record if ("NOT foo =~ .*bar.* OR hum =~ .*bug.*) the NOT bit is important
because officially you can't do NOTs with regex, so on face value this needs to be an exclude or similar
but not clear if we can do this combined statement with a normal grep.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `48fba3de86d73b78138057383dca2be423fa9c70`.  There
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
{"case_id": "fluent_fluent_bit__11326__48fba3d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
