# rust-lang/rust cut at c44324a4fe8e96f9d6473255df6c3a481caca76f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f0580df0d53d67ad5c7f85756eb9f221566e4fb0 \
        --stage baseline --out /opt/swe-time/receipt.json
