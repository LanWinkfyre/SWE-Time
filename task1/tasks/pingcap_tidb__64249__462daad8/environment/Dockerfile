# pingcap/tidb cut at bce559b421ad7436c05f61f6222e11cb6c01adbe: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 749c973e5a70e581bea535e980afe32adf5a3e11 \
        --stage baseline --out /opt/swe-time/receipt.json
