# libretro/RetroArch cut at 70daba65942d9b4695d83a28511c2e2b7e8f3d53: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d76df869b1cb40b054e27003ab72d24e3ced27a8 \
        --stage baseline --out /opt/swe-time/receipt.json
