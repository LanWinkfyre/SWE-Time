# kubernetes/kubernetes cut at a0c2788249ae1582d10089e7a34bb54fc6b3879d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 809eaa7025119712ca82c6f4dfa73a4a544ad7ec \
        --stage baseline --out /opt/swe-time/receipt.json
