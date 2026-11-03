# curl/curl cut at 02c7a2ccabf3b21f881faacf286b4308c4ace1bc: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7551e55d6614cddb039602e08f3d7aa302299617 \
        --stage baseline --out /opt/swe-time/receipt.json
