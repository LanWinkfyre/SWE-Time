# golang/go cut at fca6ad45e25647d8d156a8ecd29137000408efeb: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1d44c4e37847a975c40f8f15df7914939b540f6b \
        --stage baseline --out /opt/swe-time/receipt.json
