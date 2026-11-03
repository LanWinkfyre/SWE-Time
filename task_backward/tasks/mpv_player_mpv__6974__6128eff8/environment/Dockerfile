# mpv-player/mpv cut at 61b46d101e95ce29c680082cc11ae72c7b80e045: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0f938b197a79c09b01a9dcf39f02e95d9d7fb4a2 \
        --stage baseline --out /opt/swe-time/receipt.json
