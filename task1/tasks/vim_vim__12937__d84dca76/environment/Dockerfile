# vim/vim cut at 85c3a5bc265393c1b8b93d8b88b936d3b8b4aec7: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 93ebb5e75e564403624314c84c97293427d001d6 \
        --stage baseline --out /opt/swe-time/receipt.json
