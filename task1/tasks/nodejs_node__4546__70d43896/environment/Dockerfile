# nodejs/node cut at cc82e5e3d9aefb5e31dbe688b0038327bb7d9b80: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e51bbfd487e4ca8ebe79e423eb9aa057028cc37d \
        --stage baseline --out /opt/swe-time/receipt.json
