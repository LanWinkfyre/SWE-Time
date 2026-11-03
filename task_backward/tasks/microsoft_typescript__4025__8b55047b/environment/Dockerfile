# microsoft/TypeScript cut at 5bb2e2f584985b6b66a5ac337578fd1982f666c5: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8a2ded3cd6bd0f8e22ec58e5dd68f38b5caab56c \
        --stage baseline --out /opt/swe-time/receipt.json
