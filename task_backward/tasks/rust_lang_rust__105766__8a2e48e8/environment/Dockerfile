# rust-lang/rust cut at 7a6af2711baa5a5db116c123116b2150ed63799d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 39b2a41b39b445bf7efab02f6eade16135d7df85 \
        --stage baseline --out /opt/swe-time/receipt.json
