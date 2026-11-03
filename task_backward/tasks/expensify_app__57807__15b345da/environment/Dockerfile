# Expensify/App cut at da2fa62658cb833cfc13fc75949aa62d11fb4338: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 372de84ff02a01267d9e74891d588f737374b4d6 \
        --stage baseline --out /opt/swe-time/receipt.json
