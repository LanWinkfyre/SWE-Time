# ray-project/ray cut at 4b856fa41614f5e4ff819ec83e251c9aefd5faef: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 29e8a664c42b3107907b495b6496fb613d7d3750 \
        --stage baseline --out /opt/swe-time/receipt.json
