# bazelbuild/bazel cut at cddec1247571f1cda9939ffb7546e089e528c76e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 47ebd416ca9557898a1215428fd8720a91babbbf \
        --stage baseline --out /opt/swe-time/receipt.json
