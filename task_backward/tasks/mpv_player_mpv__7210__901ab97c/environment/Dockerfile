# mpv-player/mpv cut at 78f1629a539cc14a598831a73c59c3763c074094: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 61b8e1d436976b0d13805728c4b7f3ccd8061c90 \
        --stage baseline --out /opt/swe-time/receipt.json
