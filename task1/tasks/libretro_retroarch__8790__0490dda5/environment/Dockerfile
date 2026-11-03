# libretro/RetroArch cut at 3064d0d441bfcd2a13ff46a1a813f6c7339c4c24: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 91acb7b65ab98e676d88219d4b148ad5d88bafcf \
        --stage baseline --out /opt/swe-time/receipt.json
