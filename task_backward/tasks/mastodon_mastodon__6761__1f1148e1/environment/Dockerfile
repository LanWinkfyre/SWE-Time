# mastodon/mastodon cut at f5f165a5ebad5493a0d127c89b92876ffb75b0ef: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 051b649628d8039ff15f0c035c6f8fe5dbf045d6 \
        --stage baseline --out /opt/swe-time/receipt.json
