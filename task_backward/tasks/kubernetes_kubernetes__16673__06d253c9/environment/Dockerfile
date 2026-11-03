# kubernetes/kubernetes cut at fd03c2c1d742bba8701fe3e15338ac6302dbb351: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 62307e03d50df1025847f56e17758943dd6ab5a9 \
        --stage baseline --out /opt/swe-time/receipt.json
