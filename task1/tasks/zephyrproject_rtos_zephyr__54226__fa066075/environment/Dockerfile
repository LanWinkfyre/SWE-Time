# zephyrproject-rtos/zephyr cut at 8512bd18c66699046dffb7da0b02d72301fe8e5b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 66a4fab5719a09e52a2b45ed16570d4185923bb9 \
        --stage baseline --out /opt/swe-time/receipt.json
