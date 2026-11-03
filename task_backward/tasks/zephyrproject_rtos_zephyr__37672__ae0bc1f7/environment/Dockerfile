# zephyrproject-rtos/zephyr cut at 7ade4a23211a39ae301e33befb628f8253b56b58: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe fdc92ebb27881d4e5519105843678d13f2c79f87 \
        --stage baseline --out /opt/swe-time/receipt.json
