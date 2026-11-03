# darktable-org/darktable cut at f5720d246a8f2289c77192a9e388a137957c92fa: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe bfe82289cc7806d80afacc6c537277526b90fcab \
        --stage baseline --out /opt/swe-time/receipt.json
