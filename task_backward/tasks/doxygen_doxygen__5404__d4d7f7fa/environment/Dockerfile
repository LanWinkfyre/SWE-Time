# doxygen/doxygen cut at 154e877cc2e8b10091d7e0068b6f6d5793cd29f3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d72bfbd272669f22bfa615549dc737199a48dc95 \
        --stage baseline --out /opt/swe-time/receipt.json
