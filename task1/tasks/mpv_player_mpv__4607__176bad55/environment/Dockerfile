# mpv-player/mpv cut at 18c74f7dfe9cbefe9de818caa00c3f77ce600f71: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 60d0cea31084d770f5b2d7f691ae2aea8bc05812 \
        --stage baseline --out /opt/swe-time/receipt.json
