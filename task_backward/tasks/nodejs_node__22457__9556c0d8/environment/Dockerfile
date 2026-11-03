# nodejs/node cut at 6acb55041b53021171019ad755b72515a3712a9e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 91eec00ca20a54b1dc010cfc2fb34bc2f39eab6b \
        --stage baseline --out /opt/swe-time/receipt.json
