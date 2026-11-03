# openssl/openssl cut at 73d6b4efe6835a6c97ce61df6bf339b0903e5b7a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c7fa92979c5964966efa298bf2a40ff451ee7482 \
        --stage baseline --out /opt/swe-time/receipt.json
