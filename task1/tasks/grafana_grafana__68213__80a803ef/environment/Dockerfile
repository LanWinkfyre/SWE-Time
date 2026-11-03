# grafana/grafana cut at 5e25334663931e5d7450cbfce44e2c30d9c28ef6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b0e681c3391887fc279eb2147fe834707efae623 \
        --stage baseline --out /opt/swe-time/receipt.json
