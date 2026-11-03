# dart-lang/sdk cut at 3e12bdd717a5169ee3fa3565a97de62a2bbbd83c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8e0a669e746b5a2f4ae07f877b6f754743d8bb97 \
        --stage baseline --out /opt/swe-time/receipt.json
