# rails/rails cut at d0ce794e2d9e6f40934c2467dbf057b5e2cba88c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 965b8c372ac0e19021f92cf798095af6046ab140 \
        --stage baseline --out /opt/swe-time/receipt.json
