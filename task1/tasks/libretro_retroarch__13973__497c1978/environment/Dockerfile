# libretro/RetroArch cut at 16c0f5e223b4022698481f1ea55391f8c3f7ace2: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 98a13f386f656502df29b39e0a9a017b27bd462c \
        --stage baseline --out /opt/swe-time/receipt.json
