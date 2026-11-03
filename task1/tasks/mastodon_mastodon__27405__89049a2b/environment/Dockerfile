# mastodon/mastodon cut at e0da64bb4e0ae84fb9380b6e2bff228c997eea62: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f0ef87b84d7d56a9d59ce721062277eb58e6b3e9 \
        --stage baseline --out /opt/swe-time/receipt.json
