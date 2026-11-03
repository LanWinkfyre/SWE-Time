# highcharts/highcharts cut at 5f946d5d10789542393e55cf3cce76c3fd67b060: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6afc2d8603e2bf7c6136cd954b432cca16fb5b3d \
        --stage baseline --out /opt/swe-time/receipt.json
