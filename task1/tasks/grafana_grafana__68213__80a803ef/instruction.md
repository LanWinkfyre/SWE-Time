# Locate the commit that introduced this regression

A regression was reported against `grafana/grafana`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
encrypt-datasource-passwords:  duplicate metrics collector registration attempted

### 
# What went wrong?


**What happened**:

  - When I try to run the command `grafana-cli admin data-migration encrypt-datasource-passwords` appears an error

```bash
$ docker exec -ti grafana bash
f450704bf903:/usr/share/grafana$ grafana-cli admin data-migration encrypt-datasource-passwords
INFO [05-10|11:32:37] Starting Grafana                         logger=settings version= commit= branch= compiled=1970-01-01T00:00:00Z
WARN [05-10|11:32:37] "sentry" frontend logging provider is deprecated and will be removed in the next major version. Use "grafana" provider instead. logger=settings
INFO [05-10|11:32:37] Config loaded from                       logger=settings file=/usr/share/grafana/conf/defaults.ini
INFO [05-10|11:32:37] Config overridden from Environment variable logger=settings var="GF_PATHS_DATA=/var/lib/grafana"
INFO [05-10|11:32:37] Config overridden from Environment variable logger=settings var="GF_PATHS_LOGS=/var/log/grafana"
INFO [05-10|11:32:37] Config overridden from Environment variable logger=settings var="GF_PATHS_PLUGINS=/var/lib/grafana/plugins"
INFO [05-10|11:32:37] Config overridden from Environment variable logger=settings var="GF_PATHS_PROVISIONING=/etc/grafana/provisioning"
INFO [05-10|11:32:37] Target                                   logger=settings target=[all]
INFO [05-10|11:32:37] Path Home                                logger=settings path=/usr/share/grafana
INFO [05-10|11:32:37] Path Data                                logger=settings path=/var/lib/grafana
INFO [05-10|11:32:37] Path Logs                                logger=settings path=/var/log/grafana
INFO [05-10|11:32:37] Path Plugins                             logger=settings path=/var/lib/grafana/plugins
INFO [05-10|11:32:37] Path Provisioning                        logger=settings path=/etc/grafana/provisioning
INFO [05-10|11:32:37] App mode production                      logger=settings
INFO [05-10|11:32:37] Connecting to DB                         logger=sqlstore dbtype=sqlite3
INFO [05-10|11:32:37] Starting DB migrations                   logger=migrator
INFO [05-10|11:32:37] migrations completed                     logger=migrator performed=0 skipped=484 duration=832.607µs
INFO [05-10|11:32:37] Envelope encryption state                logger=secrets enabled=true current provider=secretKey.v1
INFO [05-10|11:32:37] Connecting to DB                         logger=sqlstore dbtype=sqlite3
INFO [05-10|11:32:37] Starting DB migrations                   logger=migrator
INFO [05-10|11:32:37] migrations completed                     logger=migrator performed=0 skipped=484 duration=534.181µs
panic: duplicate metrics collector registration attempted

goroutine 1 [running]:
github.com/prometheus/client_golang/prometheus.(*Registry).MustRegister(0x392e590?, {0xc00170ced0?, 0x1, 0xc00105c750?})
	/opt/drone/gomodcache/github.com/prometheus/client_golang@v1.14.0/prometheus/registry.go:406 +0x85
github.com/prometheus/client_golang/prometheus.MustRegister(...)
	/opt/drone/gomodcache/github.com/prometheus/client_golang@v1.14.0/prometheus/registry.go:178
github.com/grafana/grafana/pkg/services/sqlstore.ProvideService(0xc000d3e000, 0x411b080?, {0x40dbba0?, 0x61dc5f8?}, {0x40f0ae8?, 0xc00123c9a8?}, {0x40fa0f0?, 0xc001239980?})
	/drone/src/pkg/services/sqlstore/sqlstore.go:83 +0x207
github.com/grafana/grafana/pkg/cmd/grafana-cli/commands.runDbCommand.func1(0xc000b7acc0)
	/drone/src/pkg/cmd/grafana-cli/commands/commands.go:52 +0x29a
github.com/urfave/cli/v2.(*Command).Run(0x5f8d100, 0xc000b7ab80)
	/opt/drone/gomodcache/github.com/urfave/cli/v2@v2.3.0/command.go:163 +0x5c8
github.com/urfave/cli/v2.(*App).RunAsSubcommand(0xc000582340, 0xc000b7aac0)
	/opt/drone/gomodcache/github.com/urfave/cli/v2@v2.3.0/app.go:434 +0xc85
github.com/urfave/cli/v2.(*Command).startApp(0x5f8cfe0, 0xc000b7aac0)
	/opt/drone/gomodcache/github.com/urfave/cli/v2@v2.3.0/command.go:278 +0x713
github.com/urfave/cli/v2.(*Command).Run(0xc000485d30?, 0x1?)
	/opt/drone/gomodcache/github.com/urfave/cli/v2@v2.3.0/command.go:94 +0xaa
github.com/urfave/cli/v2.(*App).RunAsSubcommand(0xc0001036c0, 0xc000b7a940)
	/opt/drone/gomodcache/github.com/urfave/cli/v2@v2.3.0/app.go:434 +0xc85
github.com/urfave/cli/v2.(*Command).startApp(0x5f8e0c0, 0xc000b7a940)
	/opt/drone/gomodcache/github.com/urfave/cli/v2@v2.3.0/command.go:278 +0x713
github.com/urfave/cli/v2.(*Command).Run(0xc0002d7b00?, 0xa?)
	/opt/drone/gomodcache/github.com/urfave/cli/v2@v2.3.0/command.go:94 +0xaa
github.com/urfave/cli/v2.(*App).RunAsSubcommand(0xc000103040, 0xc000b7a600)
	/opt/drone/gomodcache/github.com/urfave/cli/v2@v2.3.0/app.go:434 +0xc85
github.com/urfave/cli/v2.(*Command).startApp(0xc0002d7560, 0xc000b7a600)
	/opt/drone/gomodcache/github.com/urfave/cli/v2@v2.3.0/command.go:278 +0x713
github.com/urfave/cli/v2.(*Command).Run(0xc00054c9e0?, 0x2?)
	/opt/drone/gomodcache/github.com/urfave/cli/v2@v2.3.0/command.go:94 +0xaa
github.com/urfave/cli/v2.(*App).RunContext(0xc00048dd40, {0x40ffc30?, 0xc000056058}, {0xc0000520a0, 0x5, 0x5})
	/opt/drone/gomodcache/github.com/urfave/cli/v2@v2.3.0/app.go:313 +0xb36
github.com/urfave/cli/v2.(*App).Run(...)
	/opt/drone/gomodcache/github.com/urfave/cli/v2@v2.3.0/app.go:224
main.main()
	/drone/src/pkg/cmd/grafana/main.go:39 +0x27d
f450704bf903:/usr/share/grafana$ grafana --version
grafana version 9.5.1
```

**What did you expect to happen**:

  - That the command runs ok, as like appears in the [documentation](https://grafana.com/docs/grafana/latest/cli/#migrate-data-and-encrypt-passwords)


### 
# How do we reproduce it?


**Step 1**:

- `docker run -d --name=grafana -p 3000:3000 grafana/grafana`

**Step 2**:

- `docker exec -ti grafana bash`

**Step 3**:

- `grafana-cli admin data-migration encrypt-datasource-passwords`


### 
# What Grafana version are you using?


9.5.1

### 
## Optional Questions:

### Is the bug inside a Dashboard Panel?


Copy the panel's ["get-help" data](https://grafana.com/docs/grafana/latest/troubleshooting/send-panel-to-grafana-support/) here

### Grafana Platform?

Docker

### User's OS?

Ubuntu 22.02

### User's Browser?

_No response_

### Is this a Regression?

None

### Are Datasources involved?

_No response_

### Anything else to add?


_No response_



I found it this way:

`test.sh`:
```sh
#!/bin/bash
make build-go && \
make build-cli && \
./bin/darwin-amd64/grafana-cli admin data-migration encrypt-datasource-passwords
```
```

## What you have

- `/testbed/repo` is a git clone of `grafana/grafana` truncated just after the regression was
  reported.  `HEAD` is `5e25334663931e5d7450cbfce44e2c30d9c28ef6` and the full history behind it is present.
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
