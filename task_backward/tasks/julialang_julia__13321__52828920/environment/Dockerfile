# JuliaLang/julia cut at 262d6babf634181c456868182f972a90240a5863: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe efab7c9691519548a47537f878e3112b0168f9f1 \
        --stage baseline --out /opt/swe-time/receipt.json
