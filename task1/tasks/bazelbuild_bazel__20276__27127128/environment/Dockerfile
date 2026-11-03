# bazelbuild/bazel cut at 08407743e903627d7e64c669f27b3f2b81316e33: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe aab19f75cd383c4b09a6ae720f9fa436bf89d271 \
        --stage baseline --out /opt/swe-time/receipt.json
