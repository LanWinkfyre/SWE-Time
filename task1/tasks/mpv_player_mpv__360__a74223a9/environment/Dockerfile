# mpv-player/mpv cut at 705a7310e6c823a72c961720f8ae416962f1398a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0f5ec05d8f4ae02262dc79a895bce3b465b376f2 \
        --stage baseline --out /opt/swe-time/receipt.json
