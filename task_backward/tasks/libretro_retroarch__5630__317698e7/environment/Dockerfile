# libretro/RetroArch cut at d1278306c75495352e50129fd9b09bcf2b883368: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b4abc39289a0abcc7d1ee6dce7e6596ba9cd15ea \
        --stage baseline --out /opt/swe-time/receipt.json
