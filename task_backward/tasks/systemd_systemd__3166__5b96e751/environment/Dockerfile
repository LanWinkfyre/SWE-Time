# systemd/systemd cut at 7178cd76f225a1c48911c68f2ae1855e97ff1397: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6738873efce1370f5db31511800138ad1768feae \
        --stage baseline --out /opt/swe-time/receipt.json
