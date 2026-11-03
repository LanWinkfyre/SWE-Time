# rails/rails cut at 574ea20dac09ff5e9879b78157c34d168ec52101: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d68e43922bc11829c52ad9f736ad5549fc97631b \
        --stage baseline --out /opt/swe-time/receipt.json
