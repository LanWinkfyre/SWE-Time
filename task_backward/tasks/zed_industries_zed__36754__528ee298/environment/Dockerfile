# zed-industries/zed cut at 3d2fa72d1fcf177e2beee1433c97e3bfa7adc09a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8204ef1e51cb89dc46415e5efe12c8705d51dfdf \
        --stage baseline --out /opt/swe-time/receipt.json
