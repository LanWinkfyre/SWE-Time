# libretro/RetroArch cut at b0f8a570b5434e798d1cddccb4c9bb2621f62c73: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 19af87214a5344c33354615114169e68c322979e \
        --stage baseline --out /opt/swe-time/receipt.json
