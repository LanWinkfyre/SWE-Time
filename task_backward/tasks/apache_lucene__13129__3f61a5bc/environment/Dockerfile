# apache/lucene cut at 8f759d5bf65079f8841224547b2b10b4c5f51f76: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 47021ae98f38612a513a30b690b96e8b05140dd5 \
        --stage baseline --out /opt/swe-time/receipt.json
