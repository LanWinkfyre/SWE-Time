# libretro/RetroArch cut at bdf5efd4ab162f8d3d50029b3f9a79fc56578c07: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe aec7ed40dad049754cc74d003f6a49da46df71d1 \
        --stage baseline --out /opt/swe-time/receipt.json
