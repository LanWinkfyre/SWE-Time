# rails/rails cut at ab06682534f63257f33ad81e4c87931e36658cb7: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7331f4fbf359e96423fad0936142b8085ae7bd40 \
        --stage baseline --out /opt/swe-time/receipt.json
