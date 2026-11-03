# cue-lang/cue cut at 43b4674898df7e2e8758ccb6154041a98e321e40: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe da3ee7dc7b27de85bbfb0a4104dfb22bcb18ef68 \
        --stage baseline --out /opt/swe-time/receipt.json
