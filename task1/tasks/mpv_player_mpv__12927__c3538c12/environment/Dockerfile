# mpv-player/mpv cut at 8faa0abae8270aedee8972070cd7c83b1cb0a095: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe bcdc5c40e71147fdacb7335471196cef3e917ec0 \
        --stage baseline --out /opt/swe-time/receipt.json
