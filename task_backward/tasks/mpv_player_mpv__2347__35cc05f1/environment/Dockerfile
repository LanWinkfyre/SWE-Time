# mpv-player/mpv cut at 6875e6a77946de2cecbdbfc6e9930a79f31767e0: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e0cb65e8ac434785f735a40ede1deb44fcb57bdb \
        --stage baseline --out /opt/swe-time/receipt.json
