# SWE-Time base image, shared by Backward (Task 1) and Forward (Task 2).
#   docker build -t swe-time/base:1 base_image/
FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        git ripgrep less ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /opt/swe-time /testbed /logs/verifier
COPY tree_digest.py probe.py view_digest.py /opt/swe-time/
WORKDIR /testbed
