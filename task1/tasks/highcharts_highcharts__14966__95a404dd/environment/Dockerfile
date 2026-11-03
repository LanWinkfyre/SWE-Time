# highcharts/highcharts cut at 1671b3875eea1385ea02df42d219f154212f760f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 3baedd8765edd17e155298d91d67dcb6e8e1878a \
        --stage baseline --out /opt/swe-time/receipt.json
