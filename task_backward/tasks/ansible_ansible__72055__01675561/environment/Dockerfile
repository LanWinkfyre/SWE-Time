# ansible/ansible cut at 672df07a338b48d10440163ac815ceec14f0c2d3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4187846fe7530166fe0f6b96877dfba185404c11 \
        --stage baseline --out /opt/swe-time/receipt.json
