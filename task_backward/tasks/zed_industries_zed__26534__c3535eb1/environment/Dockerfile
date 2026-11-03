# zed-industries/zed cut at f3f97895a93681ca0e27195ecb1b0fdd21e01042: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 47a89ad243c45df1a8aae0862ea98260c0ed7960 \
        --stage baseline --out /opt/swe-time/receipt.json
