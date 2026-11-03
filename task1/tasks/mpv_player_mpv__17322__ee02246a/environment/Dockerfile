# mpv-player/mpv cut at e99a9168c1d11bddf0530c69f578ce2a5b7d0b8f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6136c01f9580db394c73a234529d0dcc198d6ead \
        --stage baseline --out /opt/swe-time/receipt.json
