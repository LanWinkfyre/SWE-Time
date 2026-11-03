# rust-lang/rust cut at da099c2322c63144831f8585dee461e3a02e339a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 20183f498fbd8465859bf47611e1165768b9cc59 \
        --stage baseline --out /opt/swe-time/receipt.json
