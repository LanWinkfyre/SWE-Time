# curl/curl cut at 964ff76863b63516fce94d547adbbbb7d0d5c7b2: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e248439004e55425b72e42b16ec33ebe81229153 \
        --stage baseline --out /opt/swe-time/receipt.json
