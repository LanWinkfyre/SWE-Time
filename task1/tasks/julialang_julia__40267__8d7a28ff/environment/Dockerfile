# JuliaLang/julia cut at 06e7ee6ce8277035cc4ae6d0a365698f2f5bb347: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0f828a2acc497f0c26965956a57cfa9ea69cdd09 \
        --stage baseline --out /opt/swe-time/receipt.json
