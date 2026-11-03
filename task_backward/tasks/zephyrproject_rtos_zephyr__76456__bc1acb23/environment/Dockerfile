# zephyrproject-rtos/zephyr cut at 3bcaa6f8d63136ffc2ae37b6e77ee4e1cda6964f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e2549cc3c9d3c4dc4927d9a0f4ccca71d3165980 \
        --stage baseline --out /opt/swe-time/receipt.json
