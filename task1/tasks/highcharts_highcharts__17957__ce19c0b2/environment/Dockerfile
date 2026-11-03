# highcharts/highcharts cut at a0f343a71759c824743fa2c03fead7f3a36c9c4a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 432321b723e4e002ab4836dbf3d8ba748295e51d \
        --stage baseline --out /opt/swe-time/receipt.json
