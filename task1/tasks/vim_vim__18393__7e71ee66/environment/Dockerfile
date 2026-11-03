# vim/vim cut at ef818ae4448726b91c31e24406a554686dea19f5: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 900c747da393b031f3347428fb640224ac2f5442 \
        --stage baseline --out /opt/swe-time/receipt.json
