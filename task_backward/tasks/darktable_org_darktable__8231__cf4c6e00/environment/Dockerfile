# darktable-org/darktable cut at b6b4928c568bd1284d09833e5d0c3e695a958c5b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 039be44ace355d113be320690a18ba4ef878a03d \
        --stage baseline --out /opt/swe-time/receipt.json
