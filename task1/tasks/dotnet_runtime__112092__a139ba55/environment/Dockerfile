# dotnet/runtime cut at e424e0538fcafa56802d6ee23263aa0772e327d3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4fd9470900aea2fe6b0cd72aab1d3141d7540bfd \
        --stage baseline --out /opt/swe-time/receipt.json
