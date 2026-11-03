# rust-lang/rust cut at 65b448273dd280401cd440a6740a7cd891525ba3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a0c61a904482129989f5c1e5cb9f1008efb76f7f \
        --stage baseline --out /opt/swe-time/receipt.json
