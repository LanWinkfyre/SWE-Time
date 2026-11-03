# libretro/RetroArch cut at 556283a6689ab5502ceec86f4e83e8b8d796bbd8: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e37b25df88536df02446779e7cd083c3b6c541fb \
        --stage baseline --out /opt/swe-time/receipt.json
