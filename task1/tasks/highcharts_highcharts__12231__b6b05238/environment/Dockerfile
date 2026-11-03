# highcharts/highcharts cut at fa40d34b00c13fffdc858227c611a123b8878a37: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 5fbf4bd7260d6664b5f41f29dbc902a6d79fb9f5 \
        --stage baseline --out /opt/swe-time/receipt.json
