# nodejs/node cut at 03d414ed9add84541e71d180fed1b7b0609ff6c8: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2310409a89d2d76fdc87289b99011750203b79fb \
        --stage baseline --out /opt/swe-time/receipt.json
