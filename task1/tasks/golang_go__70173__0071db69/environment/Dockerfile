# golang/go cut at 989eed28497cde7145958985f50bb3dd6ab698b6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 9c93d99c616b8708bed55781915f7256051ab91e \
        --stage baseline --out /opt/swe-time/receipt.json
