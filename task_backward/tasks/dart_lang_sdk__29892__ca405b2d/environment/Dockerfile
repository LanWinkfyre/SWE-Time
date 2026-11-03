# dart-lang/sdk cut at 07725f3dfa71cd0bb056dfd275dad98ac3ae065c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8b7af73daafedacf0f239d17096703420937af69 \
        --stage baseline --out /opt/swe-time/receipt.json
