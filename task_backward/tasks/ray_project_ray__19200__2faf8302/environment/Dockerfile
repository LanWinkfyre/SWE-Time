# ray-project/ray cut at fd438d5630556a3727e7699ee3a86de5f8ffa929: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c3e3fc7637737bfb3faefe3f9f16003d9a76133e \
        --stage baseline --out /opt/swe-time/receipt.json
