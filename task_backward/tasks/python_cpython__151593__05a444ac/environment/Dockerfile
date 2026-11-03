# python/cpython cut at a064b323f4350305e7486c7b1090cf12b19e7738: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 460dec26518df5aa262ded5a2ee4e94b8854b569 \
        --stage baseline --out /opt/swe-time/receipt.json
