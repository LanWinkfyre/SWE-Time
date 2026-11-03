# rails/rails cut at 2144e70a86e6403a6298d61862e2e85615cd2a82: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e8ee2187ae910cc368e3a8bf81ed7be745fb575f \
        --stage baseline --out /opt/swe-time/receipt.json
