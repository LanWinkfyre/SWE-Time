# pandas-dev/pandas cut at c2590b346a7f8e9c0e2e7efa1d5c7318f73fa982: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe fe1bfd770f203acdbb8dbb2ccfcffa8e1c6214fc \
        --stage baseline --out /opt/swe-time/receipt.json
