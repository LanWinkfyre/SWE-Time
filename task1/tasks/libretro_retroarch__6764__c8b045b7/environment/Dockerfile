# libretro/RetroArch cut at c3c50bae299d72ba44bf577ec79060407e69197d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d2e169842658d373bbb3375ce264d8c1aa5ad9bf \
        --stage baseline --out /opt/swe-time/receipt.json
