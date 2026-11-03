# libretro/RetroArch cut at 93b29aab5ad5677202dac8004fa9b9f60034fc73: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 899d271db60aa04efa286a5225cb7c7155df7a36 \
        --stage baseline --out /opt/swe-time/receipt.json
