# rust-lang/rust cut at adbfec229ce07ff4b2a7bf2d6dec2d13cb224980: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c9bb68f5ae5cc297246a084a2cd589787d1ee315 \
        --stage baseline --out /opt/swe-time/receipt.json
