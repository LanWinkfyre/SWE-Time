# vim/vim cut at 9b16aa34b62d2e477c4ed47cb9df5a0da183e193: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe cb65fe17e96bd0d97bf61c321b79d9428647610c \
        --stage baseline --out /opt/swe-time/receipt.json
