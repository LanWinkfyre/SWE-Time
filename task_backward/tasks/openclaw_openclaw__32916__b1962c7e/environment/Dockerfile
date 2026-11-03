# openclaw/openclaw cut at 4ffe15c6b2227254e48b7724053d3c5079c9be6f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4aa548cf7de9a6c3d9620d5f1c3c4af49cece7ac \
        --stage baseline --out /opt/swe-time/receipt.json
