# cue-lang/cue cut at 407cccd9c390d7830e275e5efb60e9e7fe725e2a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0ad211955a3b8a29da269c9a64c07e4ca38ce707 \
        --stage baseline --out /opt/swe-time/receipt.json
