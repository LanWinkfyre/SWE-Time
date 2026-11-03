# cockroachdb/cockroach cut at 902401521dec9dacb9744a2a2389b241e05cfaa7: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 709881d4a1390ad68a7ddc2700c15ef6b195d928 \
        --stage baseline --out /opt/swe-time/receipt.json
