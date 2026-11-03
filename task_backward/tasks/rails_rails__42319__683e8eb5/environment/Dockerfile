# rails/rails cut at b678667853b48751ea6134f1f8ba3d687c943889: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe beb128fa88cc0e67dd69538bb2a8470cc8530747 \
        --stage baseline --out /opt/swe-time/receipt.json
