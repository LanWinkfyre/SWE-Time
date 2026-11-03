# rust-lang/rust cut at 8fbfa66b4591023d54d885fff9cdf889393af109: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4c692d3a35945d434c576c048d7066d961831980 \
        --stage baseline --out /opt/swe-time/receipt.json
