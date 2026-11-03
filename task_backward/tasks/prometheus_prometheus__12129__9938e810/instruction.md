# Locate the commit that introduced this regression

A regression was reported against `prometheus/prometheus`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
None of kubernetes jobs in up state

### What did you do?

start prometheus, access /targets in browser.


### What did you expect to see?

kubernetes related targets should all  in up state, I verified this in version v2.42.0.

### What did you see instead? Under which circumstances?

But with version v2.43.0-rc.0
[kube-state-metrics (0/2 up)]
[kubernetes-apiservers (0/3 up)]
[kubernetes-nodes (0/11 up)]
[kubernetes-nodes-cadvisor (0/11 up)]
[kubernetes-nodes-kubelet (0/11 up)]
[kubernetes-pods (0/15 up)]
[kubernetes-service-endpoints (0/8 up)]
[prometheus (1/1 up)]

### System information

Linux 3.10.0-1127.el7.x86_64 x86_64

### Prometheus version




### Prometheus configuration file

```yaml
global:
  scrape_interval:     2m
  evaluation_interval: 1m
  scrape_timeout:      30s

rule_files:
- /etc/config/rules/*.yml

alerting:
  alertmanagers:
  - static_configs:
      - targets:
        - alertmanager:80


#scrape_config_files:
#- /etc/config/scrapes/*.yml

scrape_configs:
- job_name: prometheus
  static_configs:
  - targets:
    - localhost:9090

- job_name: kubernetes-nodes
  kubernetes_sd_configs:
  - role: node
  relabel_configs:
  - action: labelmap
    regex: __meta_kubernetes_node_label_(.+)
  - action: labelmap
    regex: __meta_kubernetes_node_label_kubernetes_io_hostname
    replacement: node
  - action: replace
    source_labels:
    - __address__
    regex: (.*?):(.*?)
    target_label: __address__
    replacement: ${1}:9100

- job_name: kubernetes-apiservers
  kubernetes_sd_configs:
  - role: endpoints
    namespaces:
      names:
      - default
  relabel_configs:
  - action: keep
    regex: default;kubernetes;https
    source_labels:
    - __meta_kubernetes_namespace
    - __meta_kubernetes_service_name
    - __meta_kubernetes_endpoint_port_name
  scheme: https
  tls_config:
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    insecure_skip_verify: true
  bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

- job_name: kubernetes-nodes-kubelet
  kubernetes_sd_configs:
  - role: node
  relabel_configs:
  - action: labelmap
    regex: __meta_kubernetes_node_label_(.+)
  scheme: https
  tls_config:
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    insecure_skip_verify: true
  bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

- job_name: kubernetes-nodes-cadvisor
  kubernetes_sd_configs:
  - role: node
  relabel_configs:
  - action: labelmap
    regex: __meta_kubernetes_node_label_(.+)
  - action: replace
    target_label: __metrics_path__
    replacement: /metrics/cadvisor
  - source_labels: [instance]
    separator: ;
    regex: (.+)
    target_label: node
    replacement: $1
    action: replace
  scheme: https
  tls_config:
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    insecure_skip_verify: true
  bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

- job_name: kube-state-metrics
  kubernetes_sd_configs:
  - role: endpoints
    namespaces:
      names:
      - dtg-ops
  relabel_configs:
  - action: keep
    regex: true
    source_labels:
    - __meta_kubernetes_service_annotation_prometheus_io_scrape
  - action: keep
    source_labels:
    - __meta_kubernetes_pod_container_name
    regex: kube-state-metrics
  - action: labelmap
    regex: __meta_kubernetes_service_label_(.+)
  - action: replace
    source_labels:
    - __meta_kubernetes_namespace
    target_label: kubernetes_namespace
  - action: replace
    source_labels:
    - __meta_kubernetes_service_name
    target_label: kubernetes_service
  - action: replace
    source_labels:
    - __meta_kubernetes_pod_name
    target_label: kubernetes_pod
  - action: replace
    source_labels:
    - __meta_kubernetes_endpoints_name
    target_label: kubernetes_endpoint

- job_name: kubernetes-service-endpoints
  kubernetes_sd_configs:
  - role: endpoints
  relabel_configs:
  - action: keep
    regex: true
    source_labels:
    - __meta_kubernetes_service_annotation_prometheus_io_scrape
  - action: drop
    regex: kube-state-metrics
    source_labels:
    - __meta_kubernetes_endpoints_name
  - action: replace
    regex: (https?)
    source_labels:
    - _kubernetes_service_annotation_prometheus_io_scheme
    target_label: __scheme__
  - action: replace
    regex: (.+)
    source_labels:
    - __meta_kubernetes_service_annotation_prometheus_io_path
    target_label: __metrics_path__
  - action: replace
    regex: ([^:]+)(?::\d+)?;(\d+)
    replacement: $1:$2
    source_labels:
    - __address__
    - __meta_kubernetes_service_annotation_prometheus_io_port
    target_label: __address__
  - action: labelmap
    regex: __meta_kubernetes_service_label_(.+)
  - action: replace
    source_labels:
    - __meta_kubernetes_namespace
    target_label: kubernetes_namespace
  - action: replace
    source_labels:
    - __meta_kubernetes_service_name
    target_label: kubernetes_service_name
  - action: replace
    source_labels:
    - __meta_kubernetes_pod_name
    target_label: kubernetes_pod
  - action: replace
    source_labels:
    - __meta_kubernetes_endpoints_name
    target_label: kubernetes_endpoint

- job_name: kubernetes-services
  kubernetes_sd_configs:
  - role: service
  metrics_path: /probe
  params:
    module:
    - http_2xx
  relabel_configs:
  - action: keep
    regex: true
    source_labels:
    - __meta_kubernetes_service_annotation_prometheus_io_probe
  - source_labels:
    - __address__
    target_label: __param_target
  - replacement: blackbox
    target_label: __address__
  - source_labels:
    - __param_target
    target_label: instance
  - action: labelmap
    regex: __meta_kubernetes_service_label_(.+)
  - action: replace
    source_labels:
    - __meta_kubernetes_namespace
    target_label: kubernetes_namespace
  - action: replace
    source_labels:
    - __meta_kubernetes_service_name
    target_label: kubernetes_service_name

- job_name: kubernetes-pods
  kubernetes_sd_configs:
  - role: pod
  relabel_configs:
  - action: keep
    regex: true
    source_labels:
    - __meta_kubernetes_pod_annotation_prometheus_io_scrape
  - action: replace
    regex: (.+)
    source_labels:
    - __meta_kubernetes_pod_annotation_prometheus_io_path
    target_label: __metrics_path__
  - action: replace
    regex: ([^:]+)(?::\d+)?;(\d+)
    replacement: $1:$2
    source_labels:
    - __address__
    - __meta_kubernetes_pod_annotation_prometheus_io_port
    target_label: __address__
  - action: labelmap
    regex: __meta_kubernetes_pod_label_(.+)
  - action: replace
    source_labels:
    - __meta_kubernetes_namespace
    target_label: kubernetes_namespace
  - action: replace
    source_labels:
    - __meta_kubernetes_pod_name
    target_label: kubernetes_pod_name
```


### Alertmanager version

_No response_

### Alertmanager configuration file

_No response_

### Logs




After a couple of git bisect steps, it said:
```

## What you have

- `/testbed/repo` is a git clone of `prometheus/prometheus` truncated just after the regression was
  reported.  `HEAD` is `6c008ec56af958debf4123d7cd58a6681d17303d` and the full history behind it is present.
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
