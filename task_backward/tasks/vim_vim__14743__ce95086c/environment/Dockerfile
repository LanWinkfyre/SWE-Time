# vim/vim cut at 06bdac158072b90560915f8e664ee6d9bdab2f9b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b7deb1b69e0841cf7b7f22f57e512f17aa6c5f6c \
        --stage baseline --out /opt/swe-time/receipt.json
