# ray-project/ray cut at cc7bd6650ae88aa7fd1ce43b0ca71c869c08557a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 14d03a0869eb6eb1cf7b49f3af36c4c139c0b75d \
        --stage baseline --out /opt/swe-time/receipt.json
