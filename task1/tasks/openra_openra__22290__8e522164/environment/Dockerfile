# OpenRA/OpenRA cut at 2c0a4f5873054daac4b6f2749620b17a5a19bbea: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c47ebfbb52d70312c127c3c7bd3f5736b1fab164 \
        --stage baseline --out /opt/swe-time/receipt.json
