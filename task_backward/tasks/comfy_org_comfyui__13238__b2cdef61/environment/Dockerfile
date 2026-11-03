# Comfy-Org/ComfyUI cut at 076639fed99742f43ffbf0b0df34bb8fd105b8e9: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e2ddf28d78f190b27d136668a7dc15c7f0ec75dc \
        --stage baseline --out /opt/swe-time/receipt.json
