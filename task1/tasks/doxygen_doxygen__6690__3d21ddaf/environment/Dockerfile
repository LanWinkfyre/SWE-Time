# doxygen/doxygen cut at 449a7e2b4ff114a72be573013558bae19672ebbc: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f30a5fa78d9460550c7e921e73e11087f90b7db3 \
        --stage baseline --out /opt/swe-time/receipt.json
