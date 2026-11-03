# ansible/ansible cut at 77a47dbb2d2aa2c5b4ff2141ad34899825a144f6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 713657d6840fe5ea40fb11418eb749bd7199b8ce \
        --stage baseline --out /opt/swe-time/receipt.json
