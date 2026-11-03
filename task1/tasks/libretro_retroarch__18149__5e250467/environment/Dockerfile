# libretro/RetroArch cut at e3435221d8ffa4b69ec013658151a64d0d8fa83a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8b11aec44dde40356d291676f5ce7ea292b90d97 \
        --stage baseline --out /opt/swe-time/receipt.json
