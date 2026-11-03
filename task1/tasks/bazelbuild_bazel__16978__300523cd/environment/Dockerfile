# bazelbuild/bazel cut at 0cc796aa2722bad60f314d1b27403dc0c30bf520: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 09da33b417e798cd0059a88dcfd4634af91e6322 \
        --stage baseline --out /opt/swe-time/receipt.json
