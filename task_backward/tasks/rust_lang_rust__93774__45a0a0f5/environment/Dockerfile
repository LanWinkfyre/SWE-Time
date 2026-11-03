# rust-lang/rust cut at 775e480722c7aba6ff4ff3ccec8c1f4639ae7889: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0c292c9667f1b202a9150d58bdd2e89e3e803996 \
        --stage baseline --out /opt/swe-time/receipt.json
