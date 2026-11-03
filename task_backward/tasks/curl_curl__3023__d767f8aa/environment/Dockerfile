# curl/curl cut at ba782baac3009e44295589743bb8ae8220793e74: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2e5651a5ce0ee18d610cacfaa2b3ec5073a40c34 \
        --stage baseline --out /opt/swe-time/receipt.json
