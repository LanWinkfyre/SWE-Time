# rust-lang/rust cut at 75f9159009cd0814bd6b5c3bf6a5406de7c4fe8d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a54b5c7a645ead203d77e78245362f9e0f00dd3c \
        --stage baseline --out /opt/swe-time/receipt.json
