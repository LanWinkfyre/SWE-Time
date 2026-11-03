# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
YAML Config reserve attribute name for customer attributes

**Is your feature request related to a problem? Please describe.**
There are a variety of use cases where additional attributes in the Fluent Bit YAML file for the purposes of support processes where additional attributes would be helpful.  For example, rather than have a separate file for an OpAMP supervisor, it would make life very easy if there were a config property prefix that could be simply ignored by Fluent Bit but considered valid within the configuration file.  

This could also allow users to put config attributions into the file e.g. 
- metadata:
     usecase: 'monitor own Fluent Bit'
     configVersionNo: 12345

This sort of thing would also make it easy for a user to incorporate any annotations to the configuration that could be programmatically interogated

**Describe the solution you'd like**
Allow an attribute such as metadata to be accepted and validated as legal YAML within the configuration, but ignored by Fluent Bit itself so it has no material impact on Fluent Bit's operation. as illustrated above. Ideally, the config is checked for YAML compliance so it can be certain it is not adversely impacting the rest of the Fluent Bit setup.

**Describe alternatives you've considered**
Incorporate the information into comments - but this isn't pretty and prevents benefiting from any basic YAML validation processes.

**Additional context**
We're looking to achieve several goals:
As a minimum, track the configuration versions deployed by adding a version number tag which we can then populate on a precommit hook and/or during a deploy time consideration

ideally we can consolidate the configuration needed by an opamp supervisor within the Fluent Bit configuration file so that we don't need to maintain multiple files

<!--- Providing context helps us come up with a solution that is most useful in the real world -->
By predefining a prefix for attributes, when the ocnfiguration is being processed into Fluentbit - the standard config handler knows to exclude these attributes operationally.

<!--- Add any other context or screenshots about the feature request here. -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `117a7271c7a916990ecdad217e6111538a186a36`.  There
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
{"case_id": "fluent_fluent_bit__11683__117a727",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
