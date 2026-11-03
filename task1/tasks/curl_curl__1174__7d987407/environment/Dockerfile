# curl/curl cut at 00c817068ed9e73974b3fedf6b9d7cb085db69f4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 9aa259a139100c8d5b46b0ca9cc84bdf71e0e96b \
        --stage baseline --out /opt/swe-time/receipt.json
