# scipy/scipy cut at 012ca52084d830eab769e3fd4ac086192f1e3784: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 250d8d161b49b4dfc4a0cae2c2dc40e21aab475c \
        --stage baseline --out /opt/swe-time/receipt.json
