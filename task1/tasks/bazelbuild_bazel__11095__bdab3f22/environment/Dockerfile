# bazelbuild/bazel cut at 09924273efc7050a2e342cd89b823a619ca073f8: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1af5e991cf205c61f9fdcc9687691c3c5515122e \
        --stage baseline --out /opt/swe-time/receipt.json
