# rust-lang/rust cut at 511364e7874dba9649a264100407e4bffe7b5425: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2d64f229a09515978e6f338b821057a64334a0b5 \
        --stage baseline --out /opt/swe-time/receipt.json
