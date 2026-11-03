# ray-project/ray cut at 4183303a2f2801dd5c7cc821b98a40de7a0ef9ba: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 53d5a8a45f3972e348a13692748b65e0f9df6858 \
        --stage baseline --out /opt/swe-time/receipt.json
