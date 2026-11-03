# bazelbuild/bazel cut at cffe0e30e4949dbf2a68fb6f2747ffe14333c8a7: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 21c975d3888c6abb445a15269c1854ea46acd0bc \
        --stage baseline --out /opt/swe-time/receipt.json
