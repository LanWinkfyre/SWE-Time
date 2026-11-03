# golang/go cut at 831573cd21e65c37b4e1bf5d44dc23b125084b7a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7e63c8b765c30823131bd136d190afbe4c21abc9 \
        --stage baseline --out /opt/swe-time/receipt.json
