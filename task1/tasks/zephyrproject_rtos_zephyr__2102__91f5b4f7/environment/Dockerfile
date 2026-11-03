# zephyrproject-rtos/zephyr cut at 6a1474e75b86d65e9bf2ddf7d61c076079fe89a9: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a00625f37c5233b44b035148db13120a3c0aab69 \
        --stage baseline --out /opt/swe-time/receipt.json
