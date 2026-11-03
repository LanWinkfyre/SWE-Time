# zephyrproject-rtos/zephyr cut at 4d0a8c1e8b8316ec5071a3fcc98cd292d3bc4e6d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 563ef0d28f0da3754ed53defdfd33b630d0ed114 \
        --stage baseline --out /opt/swe-time/receipt.json
