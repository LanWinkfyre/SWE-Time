# rust-lang/rust cut at 6295686a37ed731f1059b07157170c9ac56bf8c3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 209799f3b910c64c8bd5001c0a8a55e03e7c2614 \
        --stage baseline --out /opt/swe-time/receipt.json
