# systemd/systemd cut at e6267e832bc865c5e73e9e48b6dba7d1646f8d2e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f5de77fa081b10cf31f6feb3447e062ba578e0a9 \
        --stage baseline --out /opt/swe-time/receipt.json
