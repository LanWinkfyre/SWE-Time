# highcharts/highcharts cut at c4780cb830d3180b5eb67899c42461397c0c9179: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1706b0111695d4a18574df0b4f12f8bd0d7140d5 \
        --stage baseline --out /opt/swe-time/receipt.json
