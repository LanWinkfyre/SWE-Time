# dotnet/runtime cut at ea8d8a0339bdf8b736ef5706900bab48429d1cf6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe bf7fe1d87bdb3a8b6ef6486bb03ae2f6928abf4f \
        --stage baseline --out /opt/swe-time/receipt.json
