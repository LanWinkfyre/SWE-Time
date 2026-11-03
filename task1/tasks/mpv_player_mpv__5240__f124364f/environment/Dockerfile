# mpv-player/mpv cut at 0e311fc0e8658a2c1f60bd57366c854e7fc129bc: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7fc9ff54d37aa7def8bf3cf5eb7b86b29722c129 \
        --stage baseline --out /opt/swe-time/receipt.json
