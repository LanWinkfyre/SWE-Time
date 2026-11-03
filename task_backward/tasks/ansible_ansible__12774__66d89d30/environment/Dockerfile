# ansible/ansible cut at 174ecb843c718ce70ec69cd575c36ce8e3f70ffb: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 89b0c3f6c41a50f6d2cdcefbd0f1cae0d031147c \
        --stage baseline --out /opt/swe-time/receipt.json
