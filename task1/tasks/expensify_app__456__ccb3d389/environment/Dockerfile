# Expensify/App cut at c61f211f308e6f453abc00584a84871d39079a09: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d7fd8fa437ec1fd768cabdb211aada62ec01c4ed \
        --stage baseline --out /opt/swe-time/receipt.json
