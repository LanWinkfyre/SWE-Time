# python/cpython cut at 7d1d66341838d7d1963c9ee7ffca2950d3a751fd: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f91846ba390f4437bcd525dfe6ed4355a894e159 \
        --stage baseline --out /opt/swe-time/receipt.json
