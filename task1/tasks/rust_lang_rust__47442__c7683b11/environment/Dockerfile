# rust-lang/rust cut at bb345a0be3ba3fa1970fe02789791c5c72788d8f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8ff449d505728276e822ca9a80c1e7b2da8288a2 \
        --stage baseline --out /opt/swe-time/receipt.json
