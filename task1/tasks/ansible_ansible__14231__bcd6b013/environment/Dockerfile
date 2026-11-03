# ansible/ansible cut at 49c15c81376c258d130cd0f89c6ff25467ebf17b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 633b16d11626eb220f634a6166d856b178a77e99 \
        --stage baseline --out /opt/swe-time/receipt.json
