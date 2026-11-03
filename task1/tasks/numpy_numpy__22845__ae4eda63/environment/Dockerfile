# numpy/numpy cut at 28329b2aadf87d57371fefe606df6923ada80b93: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0d1bb8e42228776dc8d35bdcfacf2ff3af366ade \
        --stage baseline --out /opt/swe-time/receipt.json
