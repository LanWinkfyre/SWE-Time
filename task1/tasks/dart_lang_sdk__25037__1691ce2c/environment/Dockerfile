# dart-lang/sdk cut at 6859412facdf673013820715723305313fba5c53: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 5b57280d5e0002469131d5c7f5a858928aef5723 \
        --stage baseline --out /opt/swe-time/receipt.json
