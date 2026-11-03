# cue-lang/cue cut at 32bfffd0aa538d63757efeef393bc37a06c8c9a4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d85f950102eef401adfad76f56d01d776e3537b9 \
        --stage baseline --out /opt/swe-time/receipt.json
