# cue-lang/cue cut at ebcf2f5b054eafd05259e79bc7dd026c2d9b76bf: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 70cc4021d459791bd4d0e493db3fdb8952f27dbe \
        --stage baseline --out /opt/swe-time/receipt.json
