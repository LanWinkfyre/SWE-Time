# python/cpython cut at bd390ef825c5f2ad86e0966173a6bcaca85a56f2: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 74761548862eb5a324c23d86a6233d884f386f2e \
        --stage baseline --out /opt/swe-time/receipt.json
