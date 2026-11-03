# rails/rails cut at a692e63bf4000cdeb9f230fb395c97edd3b12b99: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 006a82b1ad7a30b530e90e82a97c57b676974350 \
        --stage baseline --out /opt/swe-time/receipt.json
