# doxygen/doxygen cut at d062df6c56464f8063acb4fceb989e0cffdd754a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 13c270eedb4128251a1ca2efbe4d4d319c6d90ec \
        --stage baseline --out /opt/swe-time/receipt.json
