# zed-industries/zed cut at 18fcdf1d2c00d21ef6d1ccd8d771bd956cdb9687: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 00359271d11b6ba865fe81f04f675bf588a17335 \
        --stage baseline --out /opt/swe-time/receipt.json
