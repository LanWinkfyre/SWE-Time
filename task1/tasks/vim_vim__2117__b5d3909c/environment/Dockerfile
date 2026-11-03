# vim/vim cut at 1b9645de3c05f37b5c30e78f999351b0cf486ade: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f16c71b66927a28196b25a42795d083784ab1b9a \
        --stage baseline --out /opt/swe-time/receipt.json
