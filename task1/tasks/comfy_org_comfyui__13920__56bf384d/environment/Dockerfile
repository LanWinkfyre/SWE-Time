# Comfy-Org/ComfyUI cut at 04856acc699f1559a11e00a9f68d2f9f9b9b8e96: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 33ce449c8bdbb4b47935cd7d67ad90bc0c648d83 \
        --stage baseline --out /opt/swe-time/receipt.json
