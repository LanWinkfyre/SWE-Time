# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Add optional "User-Agent" header to OAuth 2.0 HTTP output plugin

**Is your feature request related to a problem? Please describe.**
Fluent Bit’s HTTP output supports OAuth 2.0 token retrieval, but it does not currently allow a User-Agent header to be set on the OAuth token request. We have encountered an OAuth provider that rejects token requests when User-Agent is missing or empty and are unable to retrieve a token. Adding optional User-Agent support for the OAuth request will improves compatibility while preserving backward compatibility for existing configurations.


**Describe the solution you'd like**
Provide the ability to add an optional `User-Agent` header in the `oauth2.*` http output plugin.
If the property is there, add the `User-Agent` header to the OAuth 2.0 HTTP Request.
If the property is absent, omit the `User-Agent` header for backwards compatibility.

Example config:
```
[OUTPUT]
    ...
    oauth2.user_agent test-agent
    ...
```

**Describe alternatives you've considered**
The only alternative is to fork fluent-bit and add the fix ourselves.

**Additional context**
We can't retrieve OAuth tokens using fluentbit HTTP from OAuth 2.0 endpoints that require a `User-Agent` header.

I have a working example of this change and have uploaded a git patch file. 
Let me know if you'd like me to submit a branch or need any other information.


[user_agent.patch](https://github.com/user-attachments/files/28021179/user_agent.patch)
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
{"case_id": "fluent_fluent_bit__11826__f6126eb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
