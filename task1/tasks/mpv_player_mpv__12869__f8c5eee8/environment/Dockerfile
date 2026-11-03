# mpv-player/mpv cut at 438ead7a3d50468b8150f2dc2727b96c78db9874: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 5db7dc08601fe857cfbc59704a2a1078d750e61e \
        --stage baseline --out /opt/swe-time/receipt.json
