# highcharts/highcharts cut at 420fc9c6f8b30b9fdccb42131020895ca08b19d4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1ebde67c5b6567db866a4a4049f78b63e4d60089 \
        --stage baseline --out /opt/swe-time/receipt.json
