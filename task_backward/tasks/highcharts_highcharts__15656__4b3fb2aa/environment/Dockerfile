# highcharts/highcharts cut at c5a840ca6c92c2f8ee3c8e10155fe8584390720e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d176bec8a9d5e96a60abbfa05a40ffe2c8dc60ee \
        --stage baseline --out /opt/swe-time/receipt.json
