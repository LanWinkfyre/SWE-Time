# apache/lucene cut at d76d55b6396d84ef7bd7c4ab2e29eab6ef497323: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6fc9d16fd0ee68fe2002497b6357b7926e416297 \
        --stage baseline --out /opt/swe-time/receipt.json
