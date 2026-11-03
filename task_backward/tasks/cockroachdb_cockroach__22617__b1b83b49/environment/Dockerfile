# cockroachdb/cockroach cut at 45ab2572599b27f0ddd456469a62470987e782a6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 679c56540f878e9c37324886a98a6e061186468a \
        --stage baseline --out /opt/swe-time/receipt.json
