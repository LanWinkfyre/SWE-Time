# bazelbuild/bazel cut at 95bbed03758a7651916d0708a892f5342a0421c5: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 666c8abb0a34a2224024b1d2168008f40fa6350f \
        --stage baseline --out /opt/swe-time/receipt.json
