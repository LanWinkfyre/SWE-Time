# libretro/RetroArch cut at 5d9934d4da8183a78286e8f6841d5f4b9ed72960: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe bcbb06c8985ef23f4879af9ee891a6790b18da51 \
        --stage baseline --out /opt/swe-time/receipt.json
