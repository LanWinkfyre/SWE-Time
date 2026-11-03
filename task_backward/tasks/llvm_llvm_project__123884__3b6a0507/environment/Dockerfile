# llvm/llvm-project cut at 65df99c208ed40271f6dcdfc29bed56540467ce7: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 527c030df8b18071553721329339326bfe82e2a5 \
        --stage baseline --out /opt/swe-time/receipt.json
