# dart-lang/sdk cut at a626c89b6a6555c211337511382ff2179700a8df: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6cd8c4eb8f51a30ab655c0638e3c5d539b5420a0 \
        --stage baseline --out /opt/swe-time/receipt.json
