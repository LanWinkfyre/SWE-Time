# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
X-Forwarded-Prefix no longer works

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**LocalAI version:** v4.0.0 (8e8b7df715e620b64d07cddf6b73bff8f966dac5)

**Environment, CPU architecture, OS, and Version:** Local Docker, x86_64, Linux Ubuntu 24.04, Docker container `localai/localai:latest-gpu-vulkan`, 

**Describe the bug**

Configured Caddy to reverse-proxy localai to local docker container with a sub-path `/localai/*`, but localai continues to return a static `/assets/` URL in response, so the sub-path `/localai/assets/` is not returned to the browser, so the page doesn't load.



**To Reproduce**

1. Configure Caddy

```
# LOCALAI_URL=/localai/*
# LOCALAI_HOST=host.docker.internal
# LOCALAI_PORT=14480
    handle_path {$LOCALAI_URL} {
        reverse_proxy {$LOCALAI_HOST}:{$LOCALAI_PORT} {
            header_up Host {upstream_hostport}
            header_up X-Forwarded-Prefix /localai
            header_up X-Forwarded-Proto https
        }
    }
```

2. Run LocalAI

3. Check response with both Caddy debug mode and curl results

```
caddy  | {"level":"debug","ts":1774574891.468641,"logger":"tls.handshake","msg":"choosing certificate","identifier":"thinkpaddy.local","num_choices":1}
caddy  | {"level":"debug","ts":1774574891.468649,"logger":"tls.handshake","msg":"custom certificate selection results","identifier":"thinkpaddy.local","subjects":["thinkpaddy.local","*.thinkpaddy.local"],"managed":false,"issuer_key":"","hash":"18d06dac5d2ae95a4b2f9882784c56a13e07dbcdef86ee6c3c3660aa73cf4f08"}
caddy  | {"level":"debug","ts":1774574891.4686568,"logger":"tls.handshake","msg":"matched certificate in cache","remote_ip":"172.20.0.1","remote_port":"46522","subjects":["thinkpaddy.local","*.thinkpaddy.local"],"managed":false,"expiration":1845694011,"hash":"18d06dac5d2ae95a4b2f9882784c56a13e07dbcdef86ee6c3c3660aa73cf4f08"}
caddy  | {"level":"debug","ts":1774574891.475979,"logger":"http.handlers.rewrite","msg":"rewrote request","request":{"remote_ip":"172.20.0.1","remote_port":"46522","client_ip":"172.20.0.1","proto":"HTTP/2.0","method":"GET","host":"thinkpaddy.local","uri":"/app","headers":{"Accept":["*/*"],"User-Agent":["curl/8.5.0"]},"tls":{"resumed":false,"version":772,"cipher_suite":4865,"proto":"h2","server_name":"thinkpaddy.local","ech":false}},"method":"GET","uri":"/app"}
caddy  | {"level":"debug","ts":1774574891.4760742,"logger":"http.handlers.reverse_proxy","msg":"selected upstream","dial":"host.docker.internal:11480","total_upstreams":1}
caddy  | {"level":"debug","ts":1774574891.477264,"logger":"http.handlers.reverse_proxy","msg":"upstream roundtrip","upstream":"host.docker.internal:11480","duration":0.001154043,"request":{"remote_ip":"172.20.0.1","remote_port":"46522","client_ip":"172.20.0.1","proto":"HTTP/2.0","method":"GET","host":"host.docker.internal:11480","uri":"/app","headers":{"User-Agent":["curl/8.5.0"],"X-Forwarded-For":["172.20.0.1"],"X-Forwarded-Proto":["https"],"X-Forwarded-Host":["thinkpaddy.local"],"Via":["2.0 Caddy"],"Accept":["*/*"],"X-Forwarded-Prefix":["/localai"]},"tls":{"resumed":false,"version":772,"cipher_suite":4865,"proto":"h2","server_name":"thinkpaddy.local","ech":false}},"headers":{"Content-Length":["848"],"Content-Type":["text/html; charset=UTF-8"],"Vary":["Origin"],"Date":["Fri, 27 Mar 2026 01:28:11 GMT"]},"status":200}
caddy  | {"level":"info","ts":1774574891.477328,"logger":"http.log.access.log0","msg":"handled request","request":{"remote_ip":"172.20.0.1","remote_port":"46522","client_ip":"172.20.0.1","proto":"HTTP/2.0","method":"GET","host":"thinkpaddy.local","uri":"/localai/app","headers":{"User-Agent":["curl/8.5.0"],"Accept":["*/*"]},"tls":{"resumed":false,"version":772,"cipher_suite":4865,"proto":"h2","server_name":"thinkpaddy.local","ech":false}},"bytes_read":0,"user_id":"","duration":0.001425003,"size":848,"status":200,"resp_headers":{"Content-Type":["text/html; charset=UTF-8"],"Vary":["Origin"],"Date":["Fri, 27 Mar 2026 01:28:11 GMT"],"Content-Length":["848"],"Via":["1.1 Caddy"],"Alt-Svc":["h3=\":443\"; ma=2592000"]}}
```

```
21:36 $ curl -s -k https://thinkpaddy.local/localai/app | grep /
  <base href="https://thinkpaddy.local/" />
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>LocalAI</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Playfair+Display:wght@400;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
    <script type="module" crossorigin src="/assets/index-jL2rWOjR.js"></script>
    <link rel="stylesheet" crossorigin href="/assets/index-Bv__f7Cv.css">
  </head>
    <div id="root"></div>
  </body>
</html>
```


**Expected behavior**

The `src="/assets/` should be `src="/localai/assets/` so that the browser will then load the page from `/localai/assets/...`


**Logs**
<!-- If applicable, add logs while running LocalAI in debug mode (`--debug` or `DEBUG=true`) to help explain your problem.  -->

**Additional context**
<!-- Add any other context about the problem here. -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `957619af53e7fc9f5dfd510d2d2ae624ed4b1917`.  There
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
{"case_id": "mudler_LocalAI__9145__957619a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
