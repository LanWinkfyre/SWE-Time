# rust-lang/rust cut at ca98712ff92c56506442cd5a500547f2f0cba0c3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f7534b566c850f860e11735b27a988dd9eec454a \
        --stage baseline --out /opt/swe-time/receipt.json
