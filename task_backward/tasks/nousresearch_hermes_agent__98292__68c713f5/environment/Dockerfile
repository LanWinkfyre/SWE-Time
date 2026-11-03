# NousResearch/hermes-agent cut at 89b38ed734ab2d5c3d263bc24fbdb8c74e931af4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0f7981b8a14ec96e7355e936ac148714c79af9c9 \
        --stage baseline --out /opt/swe-time/receipt.json
