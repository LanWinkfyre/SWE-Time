# Locate the commit that introduced this regression

A regression was reported against `grafana/grafana`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
"Query error: -1 Request was aborted" regression with 9.1.0-beta1; graphite datasource

Hello

It seems the grafana:latest docker image updated to 9.1.0-beta1 recently (I'm not 100% sure this is intended, but it's how we saw this).

Some of our panels have started breaking with "Query error: -1 Request was aborted".  I'm not sure how useful it is, but in the web developer console we get an error:

```
runRequest.catchError {"type":"cancelled","cancelled":true,"data":null,"status":-1,"statusText":"Request was aborted","config":{"method":"POST","url":"https://graphite.opendev.org/render","data":"target=scale(divideSeries(stats.gauges.afs.afs02_dfw_openstack_org.part.vicepa.used%2C%20stats.gauges.afs.afs02_dfw_openstack_org.part.vicepa.total)%2C%20100)&from=1659552968&until=1659574570&format=json&maxDataPoints=100","headers":{"Content-Type":"application/x-www-form-urlencoded"},"requestId":"OpenStack.panelId.4","inspect":{"type":"graphite"},"retry":0,"hideFromInspector":false}} react_devtools_backend.js:4026:25
    overrideMethod react_devtools_backend.js:4026
    S runRequest.ts:151
    RxJS 29
    internalFetch backend_srv.ts:127
    H ResponseQueue.ts:32
    RxJS 6
    H ResponseQueue.ts:37
    _ FetchQueueWorker.ts:56
    RxJS 21
    B FetchQueue.ts:76
    B FetchQueue.ts:55
    RxJS 6
    B FetchQueue.ts:59
    fetch backend_srv.ts:112
    RxJS 69
    pipeToSubject PanelQueryRunner.ts:290
    run PanelQueryRunner.ts:271
    runAllPanelQueries PanelModel.ts:333
    se PanelChrome.tsx:321
    RxJS 3
    n EventBus.ts:37
    emit index.js:181
    publish EventBus.ts:27
    refresh PanelModel.ts:352
    panelInitialized DashboardModel.ts:375
    componentDidMount PanelChrome.tsx:180
    React 2
    unstable_runWithPriority scheduler.production.min.js:18
    React 4
    unstable_runWithPriority scheduler.production.min.js:18
    React 4
    Redux 6
    d actions.ts:37
    Redux 2
    ue DashboardPanel.tsx:68
    c LazyLoader.tsx:24
    observer LazyLoader.tsx:58
    (Async: IntersectionCallback)
    26346 LazyLoader.tsx:55
    Webpack 14
```

![Screenshot from 2022-08-04 10-58-21](https://user-images.githubusercontent.com/108448/182740480-7eff0607-da30-4fb4-bb09-8ca99f9f84f0.png)

I have not been able to establish exactly causes this, but it does seem to be related to graphs that are using ref-id's.  This graph above shows disk usage, so it has one target that gets the total space, and then the other divides the current used space using it's refId ```A```, e.g.

```json
"targets": [
    {
      "hide": true,
      "refId": "A",
      "target": "stats.gauges.afs.afs02_dfw_openstack_org.part.vicepa.total",
      "datasource": {
        "uid": "d9c17c45a8",
        "type": "graphite"
      }
    },
    {
      "hide": false,
      "refId": "B",
      "target": "scale(divideSeries(stats.gauges.afs.afs02_dfw_openstack_org.part.vicepa.used, #A), 100)",
      "datasource": {
        "uid": "d9c17c45a8",
        "type": "graphite"
      }
    }
  ],
```

I have put some of our CI that uses this on hold so it can be inspected at https://23.253.56.172/ (note need to accept self signed certificate as it is a test system).

The panel above is https://23.253.56.172/d/9871b26303/afs?orgId=1&viewPanel=4 which exhibits the problem

https://23.253.56.172/d/9871b26303/afs?orgId=1 is the overall graph that shows some of the panels working, and others showing this error.

Everything the same works with the 9.0.6 image, so it does seem to be something introduced between then and now.



cc @bohandley
```

## What you have

- `/testbed/repo` is a git clone of `grafana/grafana` truncated just after the regression was
  reported.  `HEAD` is `fe0f19318989bd3616f68ce7546e68a4c2d6cc5f` and the full history behind it is present.
- The commit that introduced the regression is an ancestor of `HEAD`.  The commit that
  *fixes* it is not in this repository -- it was written after the cutoff.
- You do not need to build or test the project.  Reading history, `git log`, `git diff`,
  `git show` and writing your own probe scripts is the intended way to work.
- Some release-note and changelog files have been removed from the working tree on purpose.

## What to produce

Write the full 40-character hexadecimal SHA of the **first bad commit** -- the single
commit that introduced this regression -- into `/testbed/answer.txt`, and nothing else:

```
echo <40-char-sha> > /testbed/answer.txt
```

Requirements:

- Exactly one line, exactly 40 lowercase hex characters.  Abbreviated SHAs are rejected.
- No explanation, no extra lines, no surrounding punctuation.
- The commit must exist in this repository.

## Rules

- Do **not** use the network.  This task is derived from a public issue report and the
  answer is published on the internet; fetching it is cheating and is detected and
  scored zero.  Solve it from the repository.
- Do not rewrite history, add remotes, or fetch objects.
