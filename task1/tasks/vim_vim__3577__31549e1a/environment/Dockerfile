# vim/vim cut at 833e5dab143034b7e43bc0be49b2eb3687ff9ab7: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a9a8e04eab106c1d21381f79f8965fe50b94e235 \
        --stage baseline --out /opt/swe-time/receipt.json
