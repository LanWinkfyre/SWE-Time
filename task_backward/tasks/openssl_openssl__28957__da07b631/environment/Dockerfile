# openssl/openssl cut at b2ed1b72fa56e71d53af213e6e5557dcce171a2c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c2e845914a4f999183ceb950e915c5525ccdf643 \
        --stage baseline --out /opt/swe-time/receipt.json
