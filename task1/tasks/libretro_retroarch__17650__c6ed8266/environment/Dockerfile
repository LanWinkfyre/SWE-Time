# libretro/RetroArch cut at f2a86f34d136952be35cdbde42335d27cb15e774: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d862f87c28db52fe8e0940b798cd02ab4eb4274e \
        --stage baseline --out /opt/swe-time/receipt.json
