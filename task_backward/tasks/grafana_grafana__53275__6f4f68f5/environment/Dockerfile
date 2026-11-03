# grafana/grafana cut at fe0f19318989bd3616f68ce7546e68a4c2d6cc5f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2bf37a0d35d7dbcfc6cce38fa8989e6f1daa35bc \
        --stage baseline --out /opt/swe-time/receipt.json
