# doxygen/doxygen cut at 91095fb62f0bc2c624b0e8e49d9316f51be76559: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 89a9b2c55475c378fc4693904b03de65e0042f49 \
        --stage baseline --out /opt/swe-time/receipt.json
