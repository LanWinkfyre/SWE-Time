# curl/curl cut at bae555359979016999a9425a2d489f219a78abdd: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1dd71312bf6d42ca89772942665af6209e33a552 \
        --stage baseline --out /opt/swe-time/receipt.json
