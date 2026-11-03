# pingcap/tidb cut at ecbd60c3fffd76ed46613da0be89ead4bda7e06c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe eddff3429a0076dd5dec64137a3852cbc72c1997 \
        --stage baseline --out /opt/swe-time/receipt.json
