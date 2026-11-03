# neovim/neovim cut at 27a577586eace687c47e7398845178208cae524a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a494c999189200c36786f7c453c5c316244da0d1 \
        --stage baseline --out /opt/swe-time/receipt.json
