# dotnet/runtime cut at 0ca364767715fee7bc9d0273eec4f30a3c6cc8f0: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d6c2b4385305c8fda2d8e4290228f9b83005e192 \
        --stage baseline --out /opt/swe-time/receipt.json
