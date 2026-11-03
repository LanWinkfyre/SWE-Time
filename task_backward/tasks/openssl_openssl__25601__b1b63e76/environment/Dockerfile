# openssl/openssl cut at 93d1bb6dff0f0126ef1a5cac7b8693308763eb8a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 9ae1e6596f04f93d1be99c08ccfcb54f39fcc093 \
        --stage baseline --out /opt/swe-time/receipt.json
