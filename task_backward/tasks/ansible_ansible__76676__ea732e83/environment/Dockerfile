# ansible/ansible cut at b984dd9c59dd43d50f5aafa91cfde29405f2fbd9: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 094a0746b31f7ce9879dfa6fb2972930eb1cbab2 \
        --stage baseline --out /opt/swe-time/receipt.json
