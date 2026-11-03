# grafana/grafana cut at 29b3738bc8c4920af4ce0ad1cf92152c4a4ad83b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7b492d7e1610da99460cb121ec542c5b755fe6d1 \
        --stage baseline --out /opt/swe-time/receipt.json
