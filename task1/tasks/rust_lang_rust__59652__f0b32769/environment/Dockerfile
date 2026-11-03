# rust-lang/rust cut at 7641873f591dca86e2b31f60fc76b39553892631: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 546cb21f580ae3d4e0bf42ccecfad4a34defebe7 \
        --stage baseline --out /opt/swe-time/receipt.json
