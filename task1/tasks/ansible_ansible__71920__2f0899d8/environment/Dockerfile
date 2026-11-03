# ansible/ansible cut at 70e25dc15828614a1e937567c8023bf0f33b8143: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ed6fb2e3f60ac1cb472f362da8f1c7fd82fe1602 \
        --stage baseline --out /opt/swe-time/receipt.json
