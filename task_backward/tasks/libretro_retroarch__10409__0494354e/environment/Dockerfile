# libretro/RetroArch cut at e88568625c0ab210d31f02a1c0a2be0ef5a3d6f8: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 9f3a2db44e646990ff4fd06d10e3c7c8af0243d8 \
        --stage baseline --out /opt/swe-time/receipt.json
