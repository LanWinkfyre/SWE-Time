# golang/go cut at b7205b92c0a5ae985a3530dc8ad17e7d3a7a807d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7cabaded5118883a8e038df6c4365cbca4df7f1e \
        --stage baseline --out /opt/swe-time/receipt.json
