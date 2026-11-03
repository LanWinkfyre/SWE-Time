# mpv-player/mpv cut at 23843b4aa594dc8c885575f3d237cde3c29398a2: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6f009a91a6da8cd983911b890678db80b1fd40b3 \
        --stage baseline --out /opt/swe-time/receipt.json
