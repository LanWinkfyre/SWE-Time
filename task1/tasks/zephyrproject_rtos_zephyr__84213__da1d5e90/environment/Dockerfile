# zephyrproject-rtos/zephyr cut at eabef50991c3aab311ea2e9f713e7510b15b9b1e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e2d4b9878289aebf78d727317d07e4faa0065f34 \
        --stage baseline --out /opt/swe-time/receipt.json
