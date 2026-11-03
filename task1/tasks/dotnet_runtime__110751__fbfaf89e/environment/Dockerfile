# dotnet/runtime cut at b33f75519ea498df81b38fab75c4813b03c9a3e3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 373f048bae3c46810bc030ed7c1ee0568ee5ecc0 \
        --stage baseline --out /opt/swe-time/receipt.json
