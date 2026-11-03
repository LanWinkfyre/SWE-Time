# Locate the commit that introduced this regression

A regression was reported against `grafana/grafana`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Grafana keeps returning 401 if the first query to a datasource fails due to context cancelled

<!--
Please use this template to create your bug report. By providing as much info as possible you help us understand the issue, reproduce it and resolve it for you quicker. Therefore take a couple of extra minutes to make sure you have provided all info needed.

PROTIP: record your screen and attach it as a gif to showcase the issue.

- Questions should be posted to: https://community.grafana.com
- Use query inspector to troubleshoot issues: https://bit.ly/2XNF6YS
- How to record and attach gif: https://bit.ly/2Mi8T6K
-->

**What happened**:
The first request to `/api/ds/query` (Prometheus data source) failed due to context cancelled, and then Grafana started to returning status `401` to following requests 

**What you expected to happen**:
Grafana should recover after a failed request (context cancelled).

**How to reproduce it (as minimally and precisely as possible)**:
- Start a Grafana server (9.0.3) configured with a Prometheus datasource using BasicAuth
- Using the Explore page, run an arbitrary query agains the Prometheus datasource (for example `up{}`)
- Grafana works normally.
- Restart Grafana server
- Now, It's necessary that the first request to `/api/ds/query` gets context canceled. (more details on how to simulate this at the bottom)
- Grafana will return 401 for all following requests to `/api/ds/query` 

**Anything else we need to know?**:
- This issue seems to happen when:
  - the user sends a request to `/api/ds/query`
  - and the first request fails due to context cancelation
  - I am suspicious that a blank credential is being cached in somewhere, [probably here](https://github.com/grafana/grafana/blob/v9.0.3/pkg/services/pluginsettings/service/service.go#L124).
    - I think this is because [decryption does not seems to be returning an error, even if it fails](https://github.com/grafana/grafana/blob/v9.0.3/pkg/services/pluginsettings/service/service.go#L130)
  - we are seeing the following pattern at logs. 
```
ERROR[07-18|14:37:46] Failed to decrypt secure json data       logger=query_data error="context canceled"
ERROR[07-18|14:37:46] Range query failed                       logger=tsdb.prometheus query=up err="Post \"http://localhost:9090/api/v1/query_range\": context canceled"
INFO [07-18|14:37:46] Request Completed                        logger=context traceID=467f17755cf3bacd userId=1 orgId=1 uname=admin method=POST path=/api/ds/query status=400 remote_addr=127.0.0.1 time_ms=12 duration=12.371748ms size=98 referer="http://127.0.0.1:3000/explore?orgId=1&left=%7B%22datasource%22:%22grafanacloud-maiconcostay-prom%22,%22queries%22:%5B%7B%22refId%22:%22A%22,%22expr%22:%22up%22%7D%5D,%22range%22:%7B%22from%22:%22now-1h%22,%22to%22:%22now%22%7D%7D" traceID=467f17755cf3bacd  
```

In order to reproduce this, I have modified [handleQueryData](https://github.com/grafana/grafana/blob/v9.0.3/pkg/services/query/query.go#L117) to force context cancellation for the first 3 requests, this way:
```
var count = 0

func (s *Service) handleQueryData(ctx context.Context, user *models.SignedInUser, parsedReq *parsedRequest) (*backend.QueryDataResponse, error) {
	ds := parsedReq.parsedQueries[0].datasource
	if err := s.pluginRequestValidator.Validate(ds.Url, nil); err != nil {
		return nil, models.ErrDataSourceAccessDenied
	}

	// first 3 requests fail due to request cancellation
	if count < 4 {
		c, cancel := context.WithCancel(ctx)
		ctx = c
		cancel()
	}
	count++
	
	....
```

**Environment**:
- Grafana version: 9.0.3
- Data source type & version: Prometheus
- OS Grafana is installed on: Ubuntu
- User OS & Browser: Ubuntu / Chrome
- Grafana plugins: N/A
- Others: N/A

**Video**:
https://user-images.githubusercontent.com/1558179/179572509-5708de01-baad-45b0-bcce-87936faa7684.mp4




Hi, more info on this;





Full `git bisect` log:
```

## What you have

- `/testbed/repo` is a git clone of `grafana/grafana` truncated just after the regression was
  reported.  `HEAD` is `824f12a99319b443ac2d837d5c25fffb55816a1a` and the full history behind it is present.
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
