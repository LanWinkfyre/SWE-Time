# systemd/systemd cut at 3a3f71e5f09073552dd9b0de2058d8894e1bb4f9: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ce3cef2c52d928709674d8447b6c49062dd14a96 \
        --stage baseline --out /opt/swe-time/receipt.json
