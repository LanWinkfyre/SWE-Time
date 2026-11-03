# libretro/RetroArch cut at e9a264217a48b809b1dce65582ee063e33f7093a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 3cfed7ba01af179c8fd476d57450edbcb8629c63 \
        --stage baseline --out /opt/swe-time/receipt.json
