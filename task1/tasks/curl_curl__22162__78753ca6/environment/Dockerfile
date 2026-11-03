# curl/curl cut at 4ce309d968cfe02c402d07b2911241c38a8adf6b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 5232c1620897213db1781937c0bace0b7320474f \
        --stage baseline --out /opt/swe-time/receipt.json
