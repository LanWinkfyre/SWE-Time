# dart-lang/sdk cut at 208f8b5441206e562b9c8dd3dfc13015cd4fdef5: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 35fb67158bee3049b020563b0c38f83d7156f68a \
        --stage baseline --out /opt/swe-time/receipt.json
