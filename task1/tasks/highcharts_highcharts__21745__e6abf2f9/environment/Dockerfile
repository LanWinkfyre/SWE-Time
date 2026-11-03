# highcharts/highcharts cut at c38ceaf43aa37406168de9e36ca6b33959d4934c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 92304a5c1c80b3e96be634fa81b3c9c600be7cce \
        --stage baseline --out /opt/swe-time/receipt.json
