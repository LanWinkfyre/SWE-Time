# pandas-dev/pandas cut at d928a5cc222be5968b2f1f8a5f8d02977a8d6c2d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b5a963c872748801faa7ff67b8d766f7043bb1c1 \
        --stage baseline --out /opt/swe-time/receipt.json
