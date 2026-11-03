# dart-lang/sdk cut at aa345515fef6c090dcf670c719c6aebf55a8be9a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 28084d1f8503404e9fdda3efa5b27bf441aa64d3 \
        --stage baseline --out /opt/swe-time/receipt.json
