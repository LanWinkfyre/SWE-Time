# doxygen/doxygen cut at 234637167bd5d39d32bf51f755d58253441f123a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ace74cd38081c338cdc53118d324d7b7228fc4c0 \
        --stage baseline --out /opt/swe-time/receipt.json
