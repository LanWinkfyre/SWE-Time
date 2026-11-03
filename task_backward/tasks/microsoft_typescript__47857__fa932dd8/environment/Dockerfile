# microsoft/TypeScript cut at 67d376c882bcf4318a459c9a504287fc449e7847: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 77d24f93fba915bd4d509758952f3cb9187db910 \
        --stage baseline --out /opt/swe-time/receipt.json
