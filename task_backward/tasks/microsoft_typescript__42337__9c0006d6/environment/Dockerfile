# microsoft/TypeScript cut at 368cdfd29ace559e257a3c92b12212c626a5a692: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 33ea6c581a260dc217979ce59714dd0ce73ddbca \
        --stage baseline --out /opt/swe-time/receipt.json
