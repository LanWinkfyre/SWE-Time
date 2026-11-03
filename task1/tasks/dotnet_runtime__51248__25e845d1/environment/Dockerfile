# dotnet/runtime cut at b80ddefa8db351f4ed697a686d8b6ba1dd927c52: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ee0719079c4c4540f5adb135f002ad3ecf6c25ea \
        --stage baseline --out /opt/swe-time/receipt.json
