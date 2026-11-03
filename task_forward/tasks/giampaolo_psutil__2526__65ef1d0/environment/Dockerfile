# Pre-change working tree of giampaolo/psutil at 65ef1d0f8f08c992b3c7259c424cf36269955ed7, no git history.
# rebuild/rebuild.py places the tree in ./repo next to this file, so the build context is this
# environment/ directory (harbor's default).  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN python3 /opt/swe-time/tree_digest.py --repo /testbed/repo --stage baseline \
        --out /opt/swe-time/receipt.json
