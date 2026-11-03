# doxygen/doxygen cut at 509f6cc19988bb24d22c6311a4980c4353bd639d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 41539b110cb3d3793b08a643a87c146eef1bf721 \
        --stage baseline --out /opt/swe-time/receipt.json
