# rust-lang/rust cut at 956e2bcbaa00c05e051718b1375375915064f1c3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 05a7f25cc42d08aa541f50876915489bdc0eb4bb \
        --stage baseline --out /opt/swe-time/receipt.json
