# dotnet/runtime cut at 6f9d6569684cc17015aa6fc5f9d9a5f7580ade97: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2f328f19f6f9b4cb93f03f68f6bff79ed711ecc2 \
        --stage baseline --out /opt/swe-time/receipt.json
