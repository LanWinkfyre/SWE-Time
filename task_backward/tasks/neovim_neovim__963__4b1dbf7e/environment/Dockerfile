# neovim/neovim cut at e057676a89fb692f2569d7e586ea26d323428de4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b92630c2fff7950141630f0d62b11404d0589ece \
        --stage baseline --out /opt/swe-time/receipt.json
