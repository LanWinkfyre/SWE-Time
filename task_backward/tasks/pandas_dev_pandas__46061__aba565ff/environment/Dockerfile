# pandas-dev/pandas cut at 1bd193eebad6897989bbf06ae62adcffefdf97cd: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 971752a32927e78ed6f0c9ff5afca7cf82662f7a \
        --stage baseline --out /opt/swe-time/receipt.json
