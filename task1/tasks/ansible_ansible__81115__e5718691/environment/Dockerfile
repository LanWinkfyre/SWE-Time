# ansible/ansible cut at da2cd157f151ad1244296df54603698075faf5d2: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 82b5544b09057ca751f7a0991b7be3469f55ccd1 \
        --stage baseline --out /opt/swe-time/receipt.json
