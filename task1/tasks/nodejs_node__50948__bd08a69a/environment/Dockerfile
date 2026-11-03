# nodejs/node cut at 95b198911382b0aa0a0448e2a86214558665e02b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 69866bf1b68a385ba68ac4d873d89aacc37dde79 \
        --stage baseline --out /opt/swe-time/receipt.json
