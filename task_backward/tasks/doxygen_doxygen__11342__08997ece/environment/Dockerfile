# doxygen/doxygen cut at c110208ceada9325bd1611a227635487cfa95f7b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c661656f6d20a5602d7499e05d9630a74f76778a \
        --stage baseline --out /opt/swe-time/receipt.json
