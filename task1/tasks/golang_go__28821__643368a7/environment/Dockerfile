# golang/go cut at cb4130996fa7f73c62dafcd65a94233359fd9e09: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 03eb137aa311e6a5fe43f75c9f0178d042b560d9 \
        --stage baseline --out /opt/swe-time/receipt.json
