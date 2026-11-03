# rails/rails cut at 9ac6310bd988f19b02e375f1f9594df4d469f624: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0e17cf17ebeb70490d7c7cd25c6bf8f9401e44b3 \
        --stage baseline --out /opt/swe-time/receipt.json
