# mpv-player/mpv cut at 73563cebf9ae6c3c8f5ca4a84f67b2e96c08f51f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f5d545c9174216339defc222e54d419d631f5805 \
        --stage baseline --out /opt/swe-time/receipt.json
