# python/cpython cut at 0522fd81dc6e3482c2d4c8719f1f85ad5924eede: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d262250d0732bdf36cb92091e37360cf8ff40f7c \
        --stage baseline --out /opt/swe-time/receipt.json
