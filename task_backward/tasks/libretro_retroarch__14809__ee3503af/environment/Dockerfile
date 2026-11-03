# libretro/RetroArch cut at d36bd9e6778fbc1e0497a743ee5b5af019f6cb96: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b59a13771cf2903f9019af4b36f8d9217681e358 \
        --stage baseline --out /opt/swe-time/receipt.json
