# curl/curl cut at e70c22b6226badf167463029a2e1c3fe44095a64: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe bef0acaf212a71c782e0b8e8e6c772cc46040356 \
        --stage baseline --out /opt/swe-time/receipt.json
