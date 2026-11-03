# python/cpython cut at cfd31f0af20f76849bbec6185efea01c72349f2a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 5680f6546dcda550ad70eefa0a5ebf1375303307 \
        --stage baseline --out /opt/swe-time/receipt.json
