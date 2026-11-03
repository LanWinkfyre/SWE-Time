# dart-lang/sdk cut at 8c8a211c6e69f13271bc1ac0fa4f80d800be208f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1336802dee012bf341ac783faa4146b9936b68f2 \
        --stage baseline --out /opt/swe-time/receipt.json
