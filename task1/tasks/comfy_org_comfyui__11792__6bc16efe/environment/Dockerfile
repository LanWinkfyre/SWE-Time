# Comfy-Org/ComfyUI cut at dc202a2e51bf7a6cd00e606b2d2941bc223f2ad2: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6e4b1f9d00306fe14d7ca5adf2c7468d631b23d5 \
        --stage baseline --out /opt/swe-time/receipt.json
