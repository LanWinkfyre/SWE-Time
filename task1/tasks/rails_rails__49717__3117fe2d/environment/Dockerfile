# rails/rails cut at a60a5d0f5bbe30a33f8562d77277ef19906944aa: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 10d880dcd21b5eae8d8ffad99e6ee2014ae552ef \
        --stage baseline --out /opt/swe-time/receipt.json
