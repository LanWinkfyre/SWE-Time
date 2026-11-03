# darktable-org/darktable cut at f5f3c098bada9ec55bb0d44af992702f92bdbf77: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4e3bbc66e63ba06c401051307ffcaaf414d11a23 \
        --stage baseline --out /opt/swe-time/receipt.json
