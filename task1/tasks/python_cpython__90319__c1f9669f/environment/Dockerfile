# python/cpython cut at 31ff96712e8f89ac1056c2da880b44650002219f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 71ef0b4c2b77195bb1adc42602549284f7ee9566 \
        --stage baseline --out /opt/swe-time/receipt.json
