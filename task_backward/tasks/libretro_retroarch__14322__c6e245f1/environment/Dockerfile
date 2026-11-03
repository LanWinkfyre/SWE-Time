# libretro/RetroArch cut at 212013f67712f2342abfd2d585c30435e8839ae6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe cb82725cc249be5b4076f8808ca4cefe9f842485 \
        --stage baseline --out /opt/swe-time/receipt.json
