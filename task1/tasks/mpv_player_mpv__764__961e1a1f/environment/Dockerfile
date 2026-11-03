# mpv-player/mpv cut at 6589c5424ec16849c9665e8ea365d9e5ce0a88cb: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e24d736404216d01966f05656dc28d248833f894 \
        --stage baseline --out /opt/swe-time/receipt.json
