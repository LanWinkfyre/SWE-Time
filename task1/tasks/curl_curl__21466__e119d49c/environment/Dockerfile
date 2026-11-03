# curl/curl cut at a05f34973e6c4bb629d018f7cb51487be1c904d8: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ddb30354f68038629290688f4c5f58fef283727b \
        --stage baseline --out /opt/swe-time/receipt.json
