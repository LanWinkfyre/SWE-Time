# highcharts/highcharts cut at 9d8733bf3de6af7010dcfd538437da1f3c283f82: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d27c627fbe8699924194442b0b27b198a1cd37fd \
        --stage baseline --out /opt/swe-time/receipt.json
