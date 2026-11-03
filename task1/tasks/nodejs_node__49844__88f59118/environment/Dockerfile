# nodejs/node cut at c9e72e34abec1eb29fcaae3bf56fb4db76b532ec: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 5d6aa854d6dd051ac5eec6f1b9c8799ccb622a19 \
        --stage baseline --out /opt/swe-time/receipt.json
