# curl/curl cut at 811c799f2db1bbcf22e7ceee1e8c2c21525274de: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b7260c4fda95196b2fa16f32b5913f25323e5098 \
        --stage baseline --out /opt/swe-time/receipt.json
