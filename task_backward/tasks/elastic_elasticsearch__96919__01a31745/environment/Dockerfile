# elastic/elasticsearch cut at 97fd810757fd28ef1eb82776cf4c97ef894e8ad9: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 52bd463e8d73eecff8e61523b85517704fe948c2 \
        --stage baseline --out /opt/swe-time/receipt.json
