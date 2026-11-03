# golang/go cut at 213504e5431891e8421a92ab72ac08981ce07516: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 665992b5158c1c851f6e6a1ecb15a166f5ff611e \
        --stage baseline --out /opt/swe-time/receipt.json
