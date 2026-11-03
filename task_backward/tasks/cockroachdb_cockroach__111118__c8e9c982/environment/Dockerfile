# cockroachdb/cockroach cut at e9a8c49a495178fa1160cc50b1e89c802816e0c7: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ed75b08e781fc999bdb70e9933f399d7fca0dcda \
        --stage baseline --out /opt/swe-time/receipt.json
