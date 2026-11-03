# cockroachdb/cockroach cut at 04a987ecf585116bf303a6f0ff335727aa63ca1d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 304ccc770af1ed472570d8db8fc84418812e479a \
        --stage baseline --out /opt/swe-time/receipt.json
