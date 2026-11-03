# microsoft/TypeScript cut at 700ee076e515db2ef49d8cf7e4dc4bf70679575c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7901a397214e8c7b39de8954eecc707dce8cb099 \
        --stage baseline --out /opt/swe-time/receipt.json
