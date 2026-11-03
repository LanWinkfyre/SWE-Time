# numpy/numpy cut at 591880b0a7bcbb493d9ec023783157818f2f5236: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe fcbc3ba0130dd1e9b7046f934bf0ffd6ee2c362d \
        --stage baseline --out /opt/swe-time/receipt.json
