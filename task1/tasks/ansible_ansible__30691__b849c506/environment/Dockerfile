# ansible/ansible cut at f8230d961d4af427a9adbb8abf7b591b7d513f66: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0eb0d962861d356ef7e0d612834c3d549aeaea0d \
        --stage baseline --out /opt/swe-time/receipt.json
