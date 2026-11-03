# numpy/numpy cut at 954605ec08ad833899ffb956395f2d70f8eea2df: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 33f9e1fc3efc7e98bb937339273bb48e32ef527b \
        --stage baseline --out /opt/swe-time/receipt.json
