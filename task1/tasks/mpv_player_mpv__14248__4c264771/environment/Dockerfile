# mpv-player/mpv cut at 021c5dedb1f0759d6748dd6303c1fdf7f35367e4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2938ed59429a3e9cf1cf7f280cf5d13f00f236e6 \
        --stage baseline --out /opt/swe-time/receipt.json
