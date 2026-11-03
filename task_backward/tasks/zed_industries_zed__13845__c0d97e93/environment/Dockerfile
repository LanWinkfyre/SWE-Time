# zed-industries/zed cut at c8b106245c7e62353e0cd595213b166e03378130: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 56e3fc794a363896dea532346a2b9a6244b050c8 \
        --stage baseline --out /opt/swe-time/receipt.json
