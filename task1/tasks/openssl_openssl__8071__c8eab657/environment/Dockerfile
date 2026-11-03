# openssl/openssl cut at 5cae2d349b561a84dbfc93d6b6abc5fb7263fb7c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 80c455d5ae405e855391e298a2bf8a24629dd95d \
        --stage baseline --out /opt/swe-time/receipt.json
