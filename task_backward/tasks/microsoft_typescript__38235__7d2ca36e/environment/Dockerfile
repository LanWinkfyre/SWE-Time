# microsoft/TypeScript cut at d9ad27f2dd17cc1413b7d442d2915b13e0347d3e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0258db221068f096537540fa0e791a32861c3128 \
        --stage baseline --out /opt/swe-time/receipt.json
