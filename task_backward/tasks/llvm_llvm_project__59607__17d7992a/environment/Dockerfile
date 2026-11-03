# llvm/llvm-project cut at b6e344ce91c8796331fca7644eb8c748ac5391ec: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 36179ec2187a8cff935d57b6fc2d1a7585b99fcd \
        --stage baseline --out /opt/swe-time/receipt.json
