# doxygen/doxygen cut at ccf2ec4248ccf848ca694b2f031be03624105137: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c8cfa6e0246d4e73160c6099d912aa2bc24d6ef7 \
        --stage baseline --out /opt/swe-time/receipt.json
