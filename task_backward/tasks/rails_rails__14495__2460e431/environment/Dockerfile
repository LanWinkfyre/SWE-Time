# rails/rails cut at 30b94a876f32f5024f841a6de9b5b20a014a41d3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 347d74a03b137ab2e501c710c951a8b059df05ba \
        --stage baseline --out /opt/swe-time/receipt.json
