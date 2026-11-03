# libretro/RetroArch cut at e5a651789730ed5c9afcf60514e6fd2e8b308588: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 31a7f2b4d923639dca8a20393183a7d8cd71243c \
        --stage baseline --out /opt/swe-time/receipt.json
