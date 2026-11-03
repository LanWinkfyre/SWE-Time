# cue-lang/cue cut at da3ee7dc7b27de85bbfb0a4104dfb22bcb18ef68: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 33b73930b8fc8a719a88978be0b7e019ba34e247 \
        --stage baseline --out /opt/swe-time/receipt.json
