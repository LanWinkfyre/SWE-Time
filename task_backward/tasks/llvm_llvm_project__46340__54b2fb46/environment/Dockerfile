# llvm/llvm-project cut at e8b7edafc3dd0ab85903eebdfdb3bb7cc2d66743: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 09897b146a8a7cb934279e630c0027d5d4de7399 \
        --stage baseline --out /opt/swe-time/receipt.json
