# curl/curl cut at 14d5589032d5330a3d8716a9f59b85951514412d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7a19dd8a814d094cede7ca7b03e0e8b7fe7d4def \
        --stage baseline --out /opt/swe-time/receipt.json
