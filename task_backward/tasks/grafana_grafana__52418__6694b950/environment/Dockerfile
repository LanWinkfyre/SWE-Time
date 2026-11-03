# grafana/grafana cut at 824f12a99319b443ac2d837d5c25fffb55816a1a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4aae9d156719bd5bef76ae55b1834fd2178b2059 \
        --stage baseline --out /opt/swe-time/receipt.json
