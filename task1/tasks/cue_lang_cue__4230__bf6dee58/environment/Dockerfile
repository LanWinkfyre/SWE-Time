# cue-lang/cue cut at af0cfc15a7ab6e8ef67c10750c986100c12a4b96: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e7616e075c4dffcbc24971a06cf5e7877938943f \
        --stage baseline --out /opt/swe-time/receipt.json
