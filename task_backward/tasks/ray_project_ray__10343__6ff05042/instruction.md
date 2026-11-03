# Locate the commit that introduced this regression

A regression was reported against `ray-project/ray`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[core] Raylet does not start up properly on remote instance

### What is the problem?

I've started a 2 node cluster, but the remote node has to retry 10 times in order to startup.


```
rliaw@ray-gpu-docker-worker-97ecf362:/tmp/ray/session_latest/logs$ ls
log_monitor.10.err   plasma_store.11.out                                                                    raylet.11.out    reporter.1.out
log_monitor.10.out   plasma_store.12.err                                                                    raylet.12.err    reporter.2.err
log_monitor.11.err   plasma_store.12.out                                                                    raylet.12.out    reporter.2.out
log_monitor.11.out   plasma_store.1.err                                                                     raylet.1.err     reporter.3.err
log_monitor.12.err   plasma_store.1.out                                                                     raylet.1.out     reporter.3.out
log_monitor.12.out   plasma_store.2.err                                                                     raylet.2.err     reporter.4.err
log_monitor.1.err    plasma_store.2.out                                                                     raylet.2.out     reporter.4.out
log_monitor.1.out    plasma_store.3.err                                                                     raylet.3.err     reporter.5.err
log_monitor.2.err    plasma_store.3.out                                                                     raylet.3.out     reporter.5.out
log_monitor.2.out    plasma_store.4.err                                                                     raylet.4.err     reporter.6.err
log_monitor.3.err    plasma_store.4.out                                                                     raylet.4.out     reporter.6.out
log_monitor.3.out    plasma_store.5.err                                                                     raylet.5.err     reporter.7.err
log_monitor.4.err    plasma_store.5.out                                                                     raylet.5.out     reporter.7.out
log_monitor.4.out    plasma_store.6.err                                                                     raylet.6.err     reporter.8.err
log_monitor.5.err    plasma_store.6.out                                                                     raylet.6.out     reporter.8.out
log_monitor.5.out    plasma_store.7.err                                                                     raylet.7.err     reporter.9.err
log_monitor.6.err    plasma_store.7.out                                                                     raylet.7.out     reporter.9.out
log_monitor.6.out    plasma_store.8.err                                                                     raylet.8.err     reporter.err
log_monitor.7.err    plasma_store.8.out                                                                     raylet.8.out     reporter.out
log_monitor.7.out    plasma_store.9.err                                                                     raylet.9.err     worker-308de9ed75f814ffdea62d08393b3330a48e16b9-13529.err
log_monitor.8.err    plasma_store.9.out                                                                     raylet.9.out     worker-308de9ed75f814ffdea62d08393b3330a48e16b9-13529.out
log_monitor.8.out    plasma_store.err                                                                       raylet.err       worker-35d505598ecd15b326ea158ca3597109e8b84fec-13530.err
log_monitor.9.err    plasma_store.out                                                                       raylet.out       worker-35d505598ecd15b326ea158ca3597109e8b84fec-13530.out
log_monitor.9.out    python-core-worker-336a05fc3287e69c95972742c25fff720d52d688.20200826-200358.13529.log  reporter.10.err  worker-3877e3561edd1e1db1576dbbdd6f091412dc4346-0100-13528.err
log_monitor.err      python-core-worker-49f675a34a9fc5484085e1192f001ffc8e51720d.20200826-200358.13530.log  reporter.10.out  worker-3877e3561edd1e1db1576dbbdd6f091412dc4346-0100-13528.out
log_monitor.out      python-core-worker-b715d4ed0005beaa6a77909b20bb6d1fc1576ecc.20200826-200358.13528.log  reporter.11.err  worker-3877e3561edd1e1db1576dbbdd6f091412dc4346-13528.err
old                  python-core-worker-cf9cd0d5f987e7bddd7b1fd6ff0f95955c3d3779.20200826-200358.13527.log  reporter.11.out  worker-3877e3561edd1e1db1576dbbdd6f091412dc4346-13528.out
plasma_store.10.err  raylet.10.err                                                                          reporter.12.err  worker-4456bccd1793ce975b7f1144fb29665e1002f101-13527.err
plasma_store.10.out  raylet.10.out                                                                          reporter.12.out  worker-4456bccd1793ce975b7f1144fb29665e1002f101-13527.out
plasma_store.11.err  raylet.11.err                                                                          reporter.1.err
```

All of the raylet error files look like:

```
E0826 20:02:15.725277270   12954 server_chttp2.cc:40]        {"created":"@1598472135.725176780","description":"No address added out of total 1 resolved","file":"external/com_github_grpc_grpc/src/c
ore/ext/transport/chttp2/server/chttp2_server.cc","file_line":394,"referenced_errors":[{"created":"@1598472135.725174514","description":"Failed to add any wildcard listeners","file":"external/com_
github_grpc_grpc/src/core/lib/iomgr/tcp_server_posix.cc","file_line":341,"referenced_errors":[{"created":"@1598472135.725159248","description":"Unable to configure socket","fd":32,"file":"external
/com_github_grpc_grpc/src/core/lib/iomgr/tcp_server_utils_posix_common.cc","file_line":208,"referenced_errors":[{"created":"@1598472135.725152253","description":"Address already in use","errno":98
,"file":"external/com_github_grpc_grpc/src/core/lib/iomgr/tcp_server_utils_posix_common.cc","file_line":181,"os_error":"Address already in use","syscall":"bind"}]},{"created":"@1598472135.72517376
0","description":"Unable to configure socket","fd":32,"file":"external/com_github_grpc_grpc/src/core/lib/iomgr/tcp_server_utils_posix_common.cc","file_line":208,"referenced_errors":[{"created":"@1
598472135.725170986","description":"Address already in use","errno":98,"file":"external/com_github_grpc_grpc/src/core/lib/iomgr/tcp_server_utils_posix_common.cc","file_line":181,"os_error":"Addres
s already in use","syscall":"bind"}]}]}]}
*** Aborted at 1598472135 (unix time) try "date -d @1598472135" if you are using GNU date ***
PC: @                0x0 (unknown)
*** SIGSEGV (@0x55d400000058) received by PID 12954 (TID 0x7ff6e633b7c0) from PID 88; stack trace: ***
    @     0x7ff6e58990e0 (unknown)
    @     0x55d44e85c782 grpc::ServerInterface::RegisteredAsyncRequest::IssueRequest()
    @     0x55d44e4fc199 ray::rpc::ObjectManagerService::WithAsyncMethod_Push<>::RequestPush()
    @     0x55d44e50bdfb ray::rpc::ServerCallFactoryImpl<>::CreateCall()
    @     0x55d44e785c69 ray::rpc::GrpcServer::Run()
    @     0x55d44e50045e ray::ObjectManager::StartRpcService()
    @     0x55d44e510f1c ray::ObjectManager::ObjectManager()
    @     0x55d44e466162 ray::raylet::Raylet::Raylet()
    @     0x55d44e43fc3d _ZZ4mainENKUlN3ray6StatusEN5boost8optionalISt13unordered_mapISsSsSt4hashISsESt8equal_toISsESaISt4pairIKSsSsEEEEEE_clES0_SD_
    @     0x55d44e440c41 _ZNSt17_Function_handlerIFvN3ray6StatusERKN5boost8optionalISt13unordered_mapISsSsSt4hashISsESt8equal_toISsESaISt4pairIKSsSsEEEEEEZ4mainEUlS1_SE_E_E9_M_invokeERKSt9_Any_dat
aS1_SG_
    @     0x55d44e5bd6ac _ZZN3ray3gcs28ServiceBasedNodeInfoAccessor22AsyncGetInternalConfigERKSt8functionIFvNS_6StatusERKN5boost8optionalISt13unordered_mapISsSsSt4hashISsESt8equal_toISsESaISt4pair
IKSsSsEEEEEEEENKUlRKS3_RKNS_3rpc22GetInternalConfigReplyEE_clESO_SS_
    @     0x55d44e56f39f _ZNSt17_Function_handlerIFvRKN3ray6StatusERKNS0_3rpc22GetInternalConfigReplyEEZNS4_12GcsRpcClient17GetInternalConfigERKNS4_24GetInternalConfigRequestERKSt8functionIS8_EEUl
S3_S7_E_E9_M_invokeERKSt9_Any_dataS3_S7_
    @     0x55d44e56f49d ray::rpc::ClientCallImpl<>::OnReplyReceived()
    @     0x55d44e49d690 _ZN5boost4asio6detail18completion_handlerIZN3ray3rpc17ClientCallManager29PollEventsFromCompletionQueueEiEUlvE_E11do_completeEPvPNS1_19scheduler_operationERKNS_6system10err
or_codeEm
    @     0x55d44eaef54f boost::asio::detail::scheduler::do_run_one()
    @     0x55d44eaf0a51 boost::asio::detail::scheduler::run()
    @     0x55d44eaf1a82 boost::asio::io_context::run()
    @     0x55d44e421730 main
    @     0x7ff6e50ea2e1 __libc_start_main
    @     0x55d44e4328b1 (unknown)
```
*Ray version and other system information (Python version, TensorFlow version, OS):*

Latest. python=3.7.


### Reproduction (REQUIRED)
Please provide a script that can be run to reproduce the issue. The script should have **no external library dependencies** (i.e., use fake or mock data / environments):
```
# An unique identifier for the head node and workers of this cluster.
cluster_name: gpu-docker

# The minimum number of workers nodes to launch in addition to the head
# node. This number should be >= 0.
min_workers: 1

# The maximum number of workers nodes to launch in addition to the head
# node. This takes precedence over min_workers.
max_workers: 1

# The initial number of worker nodes to launch in addition to the head
# node. When the cluster is first brought up (or when it is refreshed with a
# subsequent `ray up`) this number of nodes will be started.
initial_workers: 0

# Whether or not to autoscale aggressively. If this is enabled, if at any point
#   we would start more workers, we start at least enough to bring us to
#   initial_workers.
autoscaling_mode: default

# This executes all commands on all nodes in the docker container,
# and opens all the necessary ports to support the Ray cluster.
# Empty string means disabled.
# docker:
#     image: "tensorflow/tensorflow:1.13.1-gpu-py3"
#     container_name: "ray-nvidia-docker-test" # e.g. ray_docker
#     run_options:
#       - --runtime=nvidia

    # # Example of running a GPU head with CPU workers
    # head_image: "tensorflow/tensorflow:1.13.1-gpu-py3"
    # head_run_options:
    #     - --runtime=nvidia

    # worker_image: "ubuntu:18.04"
    # worker_run_options: []


# The autoscaler will scale up the cluster to this target fraction of resource
# usage. For example, if a cluster of 10 nodes is 100% busy and
# target_utilization is 0.8, it would resize the cluster to 13. This fraction
# can be decreased to increase the aggressiveness of upscaling.
# This value must be less than 1.0 for scaling to happen.
target_utilization_fraction: 0.8

# If a node is idle for this many minutes, it will be removed.
idle_timeout_minutes: 5

# Cloud-provider specific configuration.
provider:
    type: gcp
    region: us-central1
    availability_zone: us-central1-a
    project_id: ~~~~~~~~~~~~~~ # Globally unique project id

# How Ray will authenticate with newly launched nodes.
auth:
    ssh_user: ubuntu
# By default Ray creates a new private keypair, but you can also use your own.
# If you do so, make sure to also set "KeyName" in the head and worker node
# configurations below. This requires that you have added the key into the
# project wide meta-data.
#    ssh_private_key: /path/to/your/key.pem

# Provider-specific config for the head node, e.g. instance type. By default
# Ray will auto-configure unspecified fields such as subnets and ssh-keys.
# For more documentation on available fields, see:
# https://cloud.google.com/compute/docs/reference/rest/v1/instances/insert
head_node:
    machineType: n1-standard-4
    disks:
      - boot: true
        autoDelete: true
        type: PERSISTENT
        initializeParams:
          diskSizeGb: 100
          # See https://cloud.google.com/compute/docs/images for more images
          sourceImage: projects/ml-images/global/images/c5-deeplearning-tf2-2-2-cu101-v20200701
    guestAccelerators:
      - acceleratorType: projects/~~~~~~~~~~~~~~/zones/us-central1-a/acceleratorTypes/nvidia-tesla-p4
        acceleratorCount: 1
    scheduling:
      - onHostMaintenance: TERMINATE
        preemptible: false
        automaticRestart: true
    metadata:
      - kind: compute#metadata
        items:
        - { "key": "install-nvidia-driver", "value": "True" }

    # Additional options can be found in in the compute docs at
    # https://cloud.google.com/compute/docs/reference/rest/v1/instances/insert

worker_nodes:
    machineType: n1-standard-4
    disks:
      - boot: true
        autoDelete: true
        type: PERSISTENT
        initializeParams:
          diskSizeGb: 100
          # See https://cloud.google.com/compute/docs/images for more images
          sourceImage: projects/ml-images/global/images/c5-deeplearning-tf2-2-2-cu101-v20200701
    guestAccelerators:
      - acceleratorType: projects/~~~~~~~~~~~~~~/zones/us-central1-a/acceleratorTypes/nvidia-tesla-p4
        acceleratorCount: 1
    scheduling:
      - onHostMaintenance: TERMINATE
        preemptible: false
        automaticRestart: true
    metadata:
      - kind: compute#metadata
        items:
        - { "key": "install-nvidia-driver", "value": "True" }


# Files or directories to copy to the head and worker nodes. The format is a
# dictionary from REMOTE_PATH: LOCAL_PATH, e.g.
file_mounts: {
    /home/ubuntu/train_data.txt: /Users/rliaw/dev/summit-tune-demo/train_data.txt
}


# initialization_commands:
#     # Wait until nvidia drivers are installed
#     - >-
#       timeout 300 bash -c "
#           command -v nvidia-smi && nvidia-smi
#           until [ \$? -eq 0 ]; do
#               command -v nvidia-smi && nvidia-smi
#           done"

# List of shell commands to run to set up nodes.
setup_commands:
    - source /opt/conda/bin/activate && pip install -U pip
    - source /opt/conda/bin/activate && pip install -U https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-0.9.0.dev0-cp37-cp37m-manylinux1_x86_64.whl
    - source /opt/conda/bin/activate && pip install torch==1.4.0 torchvision==0.5.0
    - source /opt/conda/bin/activate && pip install transformers
    - source /opt/conda/bin/activate && pip install wandb

# Custom commands that will be run on the head node after common setup.
head_setup_commands:
  - source /opt/conda/bin/activate && pip install google-api-python-client==1.7.8

# Custom commands that will be run on worker nodes after common setup.
worker_setup_commands: []

# Command to start ray on the head node. You don't need to change this.
head_start_ray_commands:
    - source /opt/conda/bin/activate && ray stop
    - >-
      ulimit -n 65536;
      source /opt/conda/bin/activate && ray start
      --head
      --port=6379
      --object-manager-port=8076
      --autoscaling-config=~/ray_bootstrap_config.yaml

# Command to start source /opt/conda/bin/activate && ray on worker nodes. You don't need to change this.
worker_start_ray_commands:
    - source /opt/conda/bin/activate && ray stop
    - >-
      ulimit -n 65536;
      source /opt/conda/bin/activate && ray start
      --address=$RAY_HEAD_IP:6379
      --object-manager-port=8076
```


If we cannot run your script, we cannot fix your issue.

- [ ] I have verified my script runs in a clean environment and reproduces the issue.
- [ ] I have verified the issue also occurs with the [latest wheels](https://docs.ray.io/en/latest/installation.html).


 [Here](https://gist.github.com/stephanie-wang/1fb8290e7edb630c33fe9c1dc1507814) is the test script that I used. It will hang and should continually print the stacktraces shown in the original issue if the commit is bad. You also have to make sure to first clean the cluster with `ray stop --force`, then restart again with the normal `ray stop`.
```

## What you have

- `/testbed/repo` is a git clone of `ray-project/ray` truncated just after the regression was
  reported.  `HEAD` is `4b856fa41614f5e4ff819ec83e251c9aefd5faef` and the full history behind it is present.
- The commit that introduced the regression is an ancestor of `HEAD`.  The commit that
  *fixes* it is not in this repository -- it was written after the cutoff.
- You do not need to build or test the project.  Reading history, `git log`, `git diff`,
  `git show` and writing your own probe scripts is the intended way to work.
- Some release-note and changelog files have been removed from the working tree on purpose.

## What to produce

Write the full 40-character hexadecimal SHA of the **first bad commit** -- the single
commit that introduced this regression -- into `/testbed/answer.txt`, and nothing else:

```
echo <40-char-sha> > /testbed/answer.txt
```

Requirements:

- Exactly one line, exactly 40 lowercase hex characters.  Abbreviated SHAs are rejected.
- No explanation, no extra lines, no surrounding punctuation.
- The commit must exist in this repository.

## Rules

- Do **not** use the network.  This task is derived from a public issue report and the
  answer is published on the internet; fetching it is cheating and is detected and
  scored zero.  Solve it from the repository.
- Do not rewrite history, add remotes, or fetch objects.
