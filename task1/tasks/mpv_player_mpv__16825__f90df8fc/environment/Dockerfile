# mpv-player/mpv cut at be98b35c89b42c6f094de4a97ee0a926559a5fa4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 74b47cfcb4ec510a31f1422fed758e2859fcef02 \
        --stage baseline --out /opt/swe-time/receipt.json
