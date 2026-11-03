# libretro/RetroArch cut at ce6a00b4955365a729fbb0a64f5de9c5cfc1ca10: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 793cb0cfa3fb48f8518cf5dab7ce075cd2f1f3a2 \
        --stage baseline --out /opt/swe-time/receipt.json
