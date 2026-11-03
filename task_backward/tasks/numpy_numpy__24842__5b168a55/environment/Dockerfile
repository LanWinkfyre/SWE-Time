# numpy/numpy cut at 5ca26b1b9df5e8c89923a2bb723a5ab95b6fe09b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 877522813effd8b052a3a3db8a51e5bad93d7540 \
        --stage baseline --out /opt/swe-time/receipt.json
