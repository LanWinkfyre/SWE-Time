# Expensify/App cut at 0c20881a308244867119efa6196481b65bb81274: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 811f154675aa55582a10d55491acc3f8dbfb96a5 \
        --stage baseline --out /opt/swe-time/receipt.json
