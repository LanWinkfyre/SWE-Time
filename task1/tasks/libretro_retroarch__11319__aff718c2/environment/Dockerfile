# libretro/RetroArch cut at 60b26bd490915ee0bbf169324e8f570f14b9444b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 343fef1264941adf741ac2e0b10054260cbda1bf \
        --stage baseline --out /opt/swe-time/receipt.json
