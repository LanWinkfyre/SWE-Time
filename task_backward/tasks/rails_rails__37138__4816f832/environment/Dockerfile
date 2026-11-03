# rails/rails cut at 3f27aa8cdf8c3c7f36d630f0241854f712e4c937: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6164f569e69146dfb9e85f11d06245e83d946d85 \
        --stage baseline --out /opt/swe-time/receipt.json
