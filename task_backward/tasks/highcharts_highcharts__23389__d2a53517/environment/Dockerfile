# highcharts/highcharts cut at c3cebbf82b7ea1f42455cdd6f1dfd0fb9562b0d9: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 72e941f17efc914b3064ed0ebe80f1d4f7b4770e \
        --stage baseline --out /opt/swe-time/receipt.json
