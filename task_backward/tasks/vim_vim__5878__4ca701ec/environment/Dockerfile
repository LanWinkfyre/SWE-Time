# vim/vim cut at 3cca299520a4980fd1b124564bd67782ca977c15: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 01603a9970421272621f7c1ecdc560b522c92e61 \
        --stage baseline --out /opt/swe-time/receipt.json
