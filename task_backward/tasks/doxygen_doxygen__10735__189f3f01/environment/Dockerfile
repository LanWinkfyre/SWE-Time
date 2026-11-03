# doxygen/doxygen cut at 195cfeb27bee80dcba54e84b4494b8176ce9be00: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d4ce648cb268f6205b96bc0bea40e493fd9683a3 \
        --stage baseline --out /opt/swe-time/receipt.json
