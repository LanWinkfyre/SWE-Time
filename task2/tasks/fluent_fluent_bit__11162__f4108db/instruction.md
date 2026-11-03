# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Feedback for v4.2.0 regarding function of loading TLS cert from Windows Certstore

## Bug Report

**Describe the bug**
This issue is related with new feature in v4.2.0 of https://github.com/fluent/fluent-bit/pull/11009.

After testing, the function works but with limitations.
It only could load TLS cert within Windows certstore of Root and does not support for other valid certstores. 
```
tls.windows.certstore_name: Root
```

Not sure if it is related with default values of https://github.com/fluent/fluent-bit/blob/f1ba23a2e85025de45dbf360d2970245d1a755dd/src/tls/openssl.c#L314.
As this line: https://github.com/fluent/fluent-bit/blob/f1ba23a2e85025de45dbf360d2970245d1a755dd/src/tls/openssl.c#L447 always shows "xxx from windows system Root store.".


**To Reproduce**
- Steps to reproduce the problem with similar config:

```yaml
service:
  flush_interval: 2
  log_level: debug

pipeline:
  inputs:
    - name: dummy
      tag: test

  outputs:
    - name: forward
      match: "test"
      host: 127.0.0.1
      port: 24284
      tls:  on
      tls.verify: on
      tls.vhost: localhost

      tls.windows.certstore_name:         Root/My
      tls.windows.use_enterprise_store:   false
      tls.windows.client_thumbprints:     <specific thumbprint>
```

./fluent-bit-4.2.0.exe -c test-of-above.yaml


**Expected behavior**

It is expected to load the TLS cert in certstore of My with specific thumbprint, but it failed as below snapshoot shows.

**Screenshots**

<img width="2669" height="1359" alt="Image" src="https://github.com/user-attachments/assets/6f19dcf8-5038-408f-a57c-7ba8bd8d947a" />

<img width="2659" height="948" alt="Image" src="https://github.com/user-attachments/assets/f86fd48f-1d0a-45ad-83d9-82ed026fe638" />

**Your Environment**
Windows Server 2019 Standand

**Additional context**

As screenshots shows, the thumbprint xxx17412b5b in certstore My could not be loaded. 
However, after I import it to Root, it could be loaded as expected.


**Other Request**
Indeed, our user case is using output plugin of Loki. 
The config yaml looks like:

```yaml
outputs:
  - name: loki
    xxxx: xxxx
    tls.ca_file:  <path for local CA file>
    tls.windows.certstore_name:         Root
    tls.windows.client_thumbprints:     <specific thumbprint>
    xxxx: xxx
``` 
With above WA that imported client cert to Root and I want to combine of using local file and certstore, but it failed：

<img width="2570" height="807" alt="Image" src="https://github.com/user-attachments/assets/67cd8340-5ba0-48e8-b4b8-3addcc6b511b" />

So, I just wonder that reading from file and from certstore could not be used at same time, right ? 
It is as expected per design or it could be enhanced to support this compatibility.

2> Regarding Loki, it needs another CA cert, could we add another filed such as
```
   tls.windows.ca_thumbprints:     <specific ca cert thumbprint>
```
to support reading another cert from Windows certstore ?


Appreciate for any discussion or comments.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f4108db65e876fadbabac459aa11990c5440550a`.  There
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
{"case_id": "fluent_fluent_bit__11162__f4108db",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
