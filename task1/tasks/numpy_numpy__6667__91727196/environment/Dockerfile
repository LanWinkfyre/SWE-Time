# numpy/numpy cut at 1d511429ac04d137c3d9ec7da9160bec7baa2829: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 76a75953e35b2916dfd88eaadf748c3333d0afd7 \
        --stage baseline --out /opt/swe-time/receipt.json
