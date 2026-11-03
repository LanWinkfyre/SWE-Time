# pingcap/tidb cut at 61c471487ef73f21ee453fe6ad18aaf9070d44cd: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 61eab4304eece098b8ef8297958bc0914373613c \
        --stage baseline --out /opt/swe-time/receipt.json
