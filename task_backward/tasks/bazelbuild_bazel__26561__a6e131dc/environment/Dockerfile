# bazelbuild/bazel cut at 0cd7a538d3c9a4e747e31cb96377b6ec104a1e68: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 026f01ade687a10101ecfee0d3947239880b3a6d \
        --stage baseline --out /opt/swe-time/receipt.json
