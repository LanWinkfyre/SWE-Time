# mpv-player/mpv cut at 3f5b41dfa30ca282fd99176bf879493dd72b3119: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7c9f32620f2d5f0f19130e7f6b2fa7bf38d3729b \
        --stage baseline --out /opt/swe-time/receipt.json
