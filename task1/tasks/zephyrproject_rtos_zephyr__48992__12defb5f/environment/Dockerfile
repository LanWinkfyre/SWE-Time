# zephyrproject-rtos/zephyr cut at f5378424f7f492a8ae0d173a015bc1186fcc7127: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe be21b455228905ffe368513a70bfef8a3d7b85be \
        --stage baseline --out /opt/swe-time/receipt.json
