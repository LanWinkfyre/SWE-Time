# apache/lucene cut at bea2f6750e4906adcb252ea518cf21ee867c9156: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c646d438e321472fa287be2eb41c218b114c2f9d \
        --stage baseline --out /opt/swe-time/receipt.json
