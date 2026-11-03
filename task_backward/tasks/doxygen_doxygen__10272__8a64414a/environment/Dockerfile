# doxygen/doxygen cut at 09f9ff7b98f296514dbeb4e2312849e1fb8690a9: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 719dbc315c00b0ab16220e139765a1e0ee71026f \
        --stage baseline --out /opt/swe-time/receipt.json
