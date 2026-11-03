# microsoft/TypeScript cut at 7080c4155b2c6cc69c5dae3f312d720d434da3a3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 9d53e4c5e405d25cb98fc26b6fd68f2de89d8cb9 \
        --stage baseline --out /opt/swe-time/receipt.json
