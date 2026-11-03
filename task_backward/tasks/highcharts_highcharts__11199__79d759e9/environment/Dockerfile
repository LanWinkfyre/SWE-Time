# highcharts/highcharts cut at 1f755c038050548d02f3192d2a250d82ae2cbddf: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2d50a1825e1a585b572f2b27d391a55c8bf9df61 \
        --stage baseline --out /opt/swe-time/receipt.json
