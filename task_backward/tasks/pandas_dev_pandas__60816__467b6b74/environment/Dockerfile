# pandas-dev/pandas cut at c430c613e6c712a39d07146b8adb083d55943840: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c36da3f6ded4141add4b3b16c252cedf4641e5ea \
        --stage baseline --out /opt/swe-time/receipt.json
