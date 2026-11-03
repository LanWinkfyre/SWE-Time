# cue-lang/cue cut at a44c805cc6f93e9fb32ef6ea81c2b1442c5b39ad: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 42ae8e4594a203000488dbaa1d143574fb8588c6 \
        --stage baseline --out /opt/swe-time/receipt.json
