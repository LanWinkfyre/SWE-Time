# mpv-player/mpv cut at e4b64fba9c5c6ca97189f32c056d05c2b47cebd6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 73b84595a86411ce7627e828f3e27e289cea1483 \
        --stage baseline --out /opt/swe-time/receipt.json
