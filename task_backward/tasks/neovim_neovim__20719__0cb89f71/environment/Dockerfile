# neovim/neovim cut at 4d896be681d9b93ebe34cce38a5e787cd0332261: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ef4c339fb9de87f7534303e006c281e40327f803 \
        --stage baseline --out /opt/swe-time/receipt.json
