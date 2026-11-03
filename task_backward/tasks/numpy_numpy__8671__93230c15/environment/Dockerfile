# numpy/numpy cut at f24da28e7bef4befa51354fff864bb7b5b3e07f9: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 081a865d3d243c282dc452c28dbe89e80d8bccb0 \
        --stage baseline --out /opt/swe-time/receipt.json
