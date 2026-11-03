# darktable-org/darktable cut at af2240d3999a0209f785eb0e0cc1d336734be1b4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ca8f6cb893db70656782b01d5478afe394898f1e \
        --stage baseline --out /opt/swe-time/receipt.json
