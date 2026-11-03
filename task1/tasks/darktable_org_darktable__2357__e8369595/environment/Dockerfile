# darktable-org/darktable cut at e2188ea4b3a960ac98e72d485732a6255f62f984: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 262f55c350322a2e040e690eb1deb41f374cd3dd \
        --stage baseline --out /opt/swe-time/receipt.json
