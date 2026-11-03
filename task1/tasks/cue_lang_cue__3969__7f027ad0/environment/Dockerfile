# cue-lang/cue cut at c92590272bc2b44e8e58b8f7e878281ba19c067b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 90d9b04a715744ec29a54532239ac0bdf57712e3 \
        --stage baseline --out /opt/swe-time/receipt.json
