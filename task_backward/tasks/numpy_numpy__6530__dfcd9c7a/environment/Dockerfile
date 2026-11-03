# numpy/numpy cut at 3390e440ef3563cf87eeea66ea672f8e5a6a8665: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8561c1542b42c4541f9f99ef4ad2fb8747d9943d \
        --stage baseline --out /opt/swe-time/receipt.json
