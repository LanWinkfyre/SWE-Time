# python/cpython cut at 22feeb88b473b288950cdb2f6c5d28692274b5f9: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d499031f5f33c3ef71be7c81ef52eee6b47c42e1 \
        --stage baseline --out /opt/swe-time/receipt.json
