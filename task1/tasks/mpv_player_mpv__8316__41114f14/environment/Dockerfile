# mpv-player/mpv cut at fa7afc3e19acffd3198fdc8fddb671013a337b05: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 9867f218307241961f9e7220085a9e3c23cab0af \
        --stage baseline --out /opt/swe-time/receipt.json
