# doxygen/doxygen cut at 44d739716a0e9f420958a4496188de2c6290df0e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a649da8151cb797fbd1fa72d5efc9782a5f1090a \
        --stage baseline --out /opt/swe-time/receipt.json
