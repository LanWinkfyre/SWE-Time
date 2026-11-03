# JuliaLang/julia cut at 5c312fd73afd985796201d83a3f26a3835c88b2e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e95bec60b393528d760cf2a2bd280571158b76c6 \
        --stage baseline --out /opt/swe-time/receipt.json
