# systemd/systemd cut at b72200a8a1c01ad74bdac45a0ccb3a8a6cb2e6aa: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a3ebe5eb620e49f0d24082876cafc7579261e64f \
        --stage baseline --out /opt/swe-time/receipt.json
