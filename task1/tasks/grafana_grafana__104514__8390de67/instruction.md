# Locate the commit that introduced this regression

A regression was reported against `grafana/grafana`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Dashboard provisioning: fails with a Requester was not found in the context

In the plugins-platform team we have these integration tests that check that the plugin platform at a daily interval. Yesterday we got a notification that one of our e2e tests [were failing](https://github.com/grafana/grafana-plugin-examples/actions/runs/14639984875/attempts/1).

```log
Error: Timed out 5000ms waiting for expect(locator).toHaveURL(expected)

    Locator: locator(':root')
    Expected pattern: /\/d\/Av57mRHVz\//
    Received string:  "http://localhost:[30](https://github.com/grafana/grafana-plugin-examples/actions/runs/14639984875/job/41079925454#step:35:31)00/d/Av57mRHVz"
```

Looking further into the failing e2e test I noticed that the provisioned dashboards for the app plugin wasn't provisioned correctly.






While investigating this issue I found that the dashboard provisioning for app plugins is broken but this doesn't seem to occur every time (otherwise our tests would fail more often) but I can reproduce it fairly easy:

1. requires Node >= 20
2. run `git clone https://github.com/grafana/grafana-plugin-examples.git`
3. run `cd grafana-plugin-examples/examples/app-with-dashboards`
4. run `npm install`
5. run `npm run build`
6. run `GRAFANA_VERSION=12.0.0-237754 GRAFANA_IMAGE=grafana-dev npm run server`
7. navigate to `http://localhost:3000/dashboards` you should see two example dashboards, so this commit/image works ✅ 
8. stop the docker container and run docker compose down
9. run `GRAFANA_VERSION=12.0.0-237767 GRAFANA_IMAGE=grafana-dev npm run server`
10.navigate to `http://localhost:3000/dashboards` you should see two example dashboards, but there are none, so this commit/image doesn't work 🛑  

Looking at the logs from 12.0.0-237754 we can see the following
```log
app-dashboards  | logger=provisioning.plugins t=2025-04-25T08:37:37.104277971Z level=info msg="Updating app from configuration " type=myorg-dashboard-app enabled=true
app-dashboards  | logger=plugindashboards t=2025-04-25T08:37:37.106303846Z level=info msg="Plugin state changed" pluginId=myorg-dashboard-app enabled=true
app-dashboards  | logger=plugindashboards t=2025-04-25T08:37:37.106318262Z level=info msg="Syncing plugin dashboards to DB" pluginId=myorg-dashboard-app
app-dashboards  | logger=plugindashboards t=2025-04-25T08:37:37.107204137Z level=info msg="Auto updating App dashboard" dashboard=example-dashboard-1 newRev=1 oldRev=0
app-dashboards  | logger=plugindashboards t=2025-04-25T08:37:37.125321346Z level=info msg="Auto updating App dashboard" dashboard=example-dashboard-2 newRev=1 oldRev=0
```

Looking at the logs from 12.0.0-237767 we can see the following `Failed to load app dashboards a Requester was not found in the context`
```log
app-dashboards  | logger=provisioning.plugins t=2025-04-25T08:36:37.305057388Z level=info msg="Updating app from configuration " type=myorg-dashboard-app enabled=true
app-dashboards  | logger=plugindashboards t=2025-04-25T08:36:37.306635304Z level=info msg="Plugin state changed" pluginId=myorg-dashboard-app enabled=true
app-dashboards  | logger=plugindashboards t=2025-04-25T08:36:37.306648846Z level=info msg="Syncing plugin dashboards to DB" pluginId=myorg-dashboard-app
app-dashboards  | logger=plugindashboards t=2025-04-25T08:36:37.306659429Z level=error msg="Failed to load app dashboards" error="a Requester was not found in the context"
```

There is a work around and that is to go to the settings page for the plugin and Disable/Enable the plugin then the dashboards are provisioned correctly.
```

## What you have

- `/testbed/repo` is a git clone of `grafana/grafana` truncated just after the regression was
  reported.  `HEAD` is `29b3738bc8c4920af4ce0ad1cf92152c4a4ad83b` and the full history behind it is present.
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
