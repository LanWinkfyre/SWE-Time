# pingcap/tidb cut at a0f2405981960ec705bf44f12b96ca8aec1506c4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b384b73f2137b24a67c8871245e67963b6731139 \
        --stage baseline --out /opt/swe-time/receipt.json
