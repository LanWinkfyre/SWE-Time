# libretro/RetroArch cut at a99a7deab1d9a249f2347ce79b8d7e06be8386ce: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c03deadb12fcebf3267d5ba9354a6b5f3655ded6 \
        --stage baseline --out /opt/swe-time/receipt.json
