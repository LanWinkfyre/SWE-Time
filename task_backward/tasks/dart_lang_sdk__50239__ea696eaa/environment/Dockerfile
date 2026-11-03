# dart-lang/sdk cut at 204c03a98ed42afe65068e3efe931ff5b890158c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe fee8a22c31333b2e04c0ae1971966c10dcb7847f \
        --stage baseline --out /opt/swe-time/receipt.json
