# zephyrproject-rtos/zephyr cut at ccd88a4b611ca4dfe3985709d3cd36021910a6c2: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 40ec70fd2ad5ab52bfa077066d04c994e6a33987 \
        --stage baseline --out /opt/swe-time/receipt.json
