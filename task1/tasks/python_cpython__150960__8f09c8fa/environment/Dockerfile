# python/cpython cut at e4db68b9c990ed1bb7562094bee2e73f4450d42b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 49f4ecfb08e6192ddc9f782553c775ccbdc2dfdb \
        --stage baseline --out /opt/swe-time/receipt.json
