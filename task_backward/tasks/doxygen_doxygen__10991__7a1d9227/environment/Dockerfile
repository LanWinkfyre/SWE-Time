# doxygen/doxygen cut at 93ad49251c5f273a7a276e22ef2f8ef48afdd86c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 269d60d6057f67b587e491ef5b1336fd071b96a8 \
        --stage baseline --out /opt/swe-time/receipt.json
