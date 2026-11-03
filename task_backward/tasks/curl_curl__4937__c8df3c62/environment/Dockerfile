# curl/curl cut at 4a4b63daaa01ef59b131d91e8e6e6dfe275c0f08: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 3ea15be3f3d6c77adc9fe22ad0b0208466d622d1 \
        --stage baseline --out /opt/swe-time/receipt.json
