# highcharts/highcharts cut at e0b0d6411d9bd81a09357f7b752e26b0296bb507: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4385dbd2668eec56ebfae19a65881e3c03682c34 \
        --stage baseline --out /opt/swe-time/receipt.json
