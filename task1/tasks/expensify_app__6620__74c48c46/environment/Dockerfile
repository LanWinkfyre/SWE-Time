# Expensify/App cut at 673869099b13acfd28ebf798c3c44e075314bb31: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 3b5c680aaf14719c440901b7258843be1e400ef6 \
        --stage baseline --out /opt/swe-time/receipt.json
