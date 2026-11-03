# mastodon/mastodon cut at 402ee73e24ea816ab1602405cd0046ecd5e7bfd5: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 99a43f0282d5115b75a564205ca7d2db31a3a945 \
        --stage baseline --out /opt/swe-time/receipt.json
