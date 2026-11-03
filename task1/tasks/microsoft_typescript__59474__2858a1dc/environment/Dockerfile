# microsoft/TypeScript cut at d7ff565b6c3057f844d007d5417ec84d5aafda87: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 356867908c2dc9efc627925abdb9d3b510e0a34a \
        --stage baseline --out /opt/swe-time/receipt.json
