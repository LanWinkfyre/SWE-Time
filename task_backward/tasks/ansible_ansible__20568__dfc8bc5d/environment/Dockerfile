# ansible/ansible cut at 43519c9bef1ecf0dd4a3d0839578e04c85e90a1d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f86e6a21522ee8469390dc7fc220f72f60972a7c \
        --stage baseline --out /opt/swe-time/receipt.json
