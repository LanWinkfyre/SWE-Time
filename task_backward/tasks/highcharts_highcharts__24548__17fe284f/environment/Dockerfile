# highcharts/highcharts cut at aae8e928fd0b9d7705d49860b31142ea13e35535: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 31cfde6bbbad1dc1697ecc6e506591aeeff30a4d \
        --stage baseline --out /opt/swe-time/receipt.json
