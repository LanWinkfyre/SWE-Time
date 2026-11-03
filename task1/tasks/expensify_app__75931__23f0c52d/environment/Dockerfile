# Expensify/App cut at 3f1a831f7ce5305993f44b3da7571fbd063ce7c5: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 90ca5a8dec8eb33146a9e38c6555541fe8a1f933 \
        --stage baseline --out /opt/swe-time/receipt.json
