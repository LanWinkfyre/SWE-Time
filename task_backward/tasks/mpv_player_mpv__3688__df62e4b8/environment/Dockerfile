# mpv-player/mpv cut at a2fa0d0b68ce200598122145254f56ae1adff91e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 768448305292f50c72533597c25992b70e8e42ac \
        --stage baseline --out /opt/swe-time/receipt.json
