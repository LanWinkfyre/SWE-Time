# vim/vim cut at 2e4cb3b042faba5efc9b5a8b4f86942a417494ce: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4f1982800f0aff28df6875e718a786f6c4b11ad9 \
        --stage baseline --out /opt/swe-time/receipt.json
