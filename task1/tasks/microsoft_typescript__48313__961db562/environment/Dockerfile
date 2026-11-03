# microsoft/TypeScript cut at b996287e00088f0dcdf138b363a4b84d4b98a403: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe df1faa09b8b8609c110507743ee98ce64cc612b6 \
        --stage baseline --out /opt/swe-time/receipt.json
