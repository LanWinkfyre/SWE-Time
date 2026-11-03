# mpv-player/mpv cut at bca59516cc172e72a606b01b783added9c45dfb8: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 157b24228994ebc2283ce47c8fb0c5b3af5a83e6 \
        --stage baseline --out /opt/swe-time/receipt.json
