# zephyrproject-rtos/zephyr cut at a78e7c5c90d8cb31ec550ce289503bd698675585: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe efbe031aa5741a46ef064789bd15e06fd1244b85 \
        --stage baseline --out /opt/swe-time/receipt.json
