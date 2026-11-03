# zephyrproject-rtos/zephyr cut at e01a4df3fb8d4052addf2cd8db110e7f61e09c3e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c27561d984daa3bd83faf376d0eff6ccdf761269 \
        --stage baseline --out /opt/swe-time/receipt.json
