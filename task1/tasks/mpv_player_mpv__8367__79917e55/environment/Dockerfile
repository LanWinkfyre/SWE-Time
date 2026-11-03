# mpv-player/mpv cut at a9aa5a1b1cf3573a219dec2b98aea06d3b866908: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d479dfd67de910d2a8abf876cd2d99cc2e62c2ea \
        --stage baseline --out /opt/swe-time/receipt.json
