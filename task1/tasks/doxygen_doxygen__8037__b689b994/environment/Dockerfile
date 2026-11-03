# doxygen/doxygen cut at 0fc06d657d596adcc289a5f228973ea268efd66d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe bdb9c1141a712d7309c22084f2d45c22ecc31aed \
        --stage baseline --out /opt/swe-time/receipt.json
