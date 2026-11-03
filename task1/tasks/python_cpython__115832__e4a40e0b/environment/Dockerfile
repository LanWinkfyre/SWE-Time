# python/cpython cut at 17dab2e572141a4295325bf7019301fece301fe1: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a3859422d15d98892fd53499916bd424f841404f \
        --stage baseline --out /opt/swe-time/receipt.json
