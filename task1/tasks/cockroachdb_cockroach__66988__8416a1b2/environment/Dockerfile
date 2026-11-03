# cockroachdb/cockroach cut at 858fc125ebb5585120a42fd415058b8f9db76df3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 045d42e56df9c93326558174bc59eba20251b882 \
        --stage baseline --out /opt/swe-time/receipt.json
