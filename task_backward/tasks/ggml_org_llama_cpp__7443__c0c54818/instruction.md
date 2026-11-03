# Locate the commit that introduced this regression

A regression was reported against `ggml-org/llama.cpp`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Performance Regression Observed in llama.cpp

We have observed a performance regression in llama.cpp when using FP32 kernels. The regression is significant, and we would like to investigate the cause and propose possible solutions. 

  

### Background:
When MKL Verbose logs are printed, we see that llama.cpp uses FP32 kernels for all models of various precision. Looks like usage of INT8 kernels may give a huge boost to the performance. But the observed performance regression suggests that there may be underlying issues that need to be addressed.

### Steps to Reproduce

Running   ./llama-bench -m ./llama-2-7b-q8_0.gguf -t 96 -p 512 -b 512 -n 60 to get numbers. 

### Questions
- Integrate BF16 kernels: Integrate BF16/INT8 kernels from DNN libraries to reduce memory usage and improve performance.
- Support for INT8 kernels: How are the weights converted to FP32 from INT8? Is it a separate memory pass, if yes, why isn't the overhead coming on the performance (when compared to a PyTorch based setup)? Or with INT8 kernels, would it be possible to see higher performance?
- Memory-intensive cast operator: Do we use a cast operator for dequantization? The cast operator for dequantizing INT8 weights to FP32 is memory-intensive and can bottleneck the performance.
- Separate memory pass for weights: The weights are passed as a separate memory pass, which can increase the memory access pattern and potentially impact performance. 


I am also seeing a large performance regression on L2 70B at Q5, which is a very common model.
I ran git bisect and found the following results:







| model                          |       size |     params | backend    |    threads |          test |              t/s |
| ------------------------------ | ---------: | ---------: | ---------- | ---------: | ------------: | ---------------: |
| llama 70B Q5_K - Medium        |  45.40 GiB |    68.98 B | CPU        |         64 |         pp512 |     17.57 ± 0.04 |
| llama 70B Q5_K - Medium        |  45.40 GiB |    68.98 B | CPU        |         64 |         tg128 |      4.52 ± 0.04 |

| llama 70B Q5_K - Medium        |  45.40 GiB |    68.98 B | CPU        |         64 | pp 512     |     17.51 ± 0.14 |
| llama 70B Q5_K - Medium        |  45.40 GiB |    68.98 B | CPU        |         64 | tg 128     |      5.77 ± 0.03 |

| llama 70B Q5_K - Medium        |  45.40 GiB |    68.98 B | CPU        |         64 | pp 512     |     17.04 ± 0.92 |
| llama 70B Q5_K - Medium        |  45.40 GiB |    68.98 B | CPU        |         64 | tg 128     |      5.35 ± 0.16 |

| llama 70B Q5_K - Medium        |  45.40 GiB |    68.98 B | CPU        |         64 |         pp512 |     17.87 ± 0.34 |
| llama 70B Q5_K - Medium        |  45.40 GiB |    68.98 B | CPU        |         64 |         tg128 |      6.34 ± 0.01 |

| llama 70B Q5_K - Medium        |  45.40 GiB |    68.98 B | CPU        |         64 |         pp512 |     18.26 ± 0.06 |
| llama 70B Q5_K - Medium        |  45.40 GiB |    68.98 B | CPU        |         64 |         tg128 |      6.47 ± 0.02 |

| llama 70B Q5_K - Medium        |  45.40 GiB |    68.98 B | CPU        |         64 |         pp512 |     18.37 ± 0.05 |
| llama 70B Q5_K - Medium        |  45.40 GiB |    68.98 B | CPU        |         64 |         tg128 |      6.76 ± 0.02 |

| llama 70B Q5_K - Medium        |  45.40 GiB |    68.98 B | CPU        |         64 |         pp512 |     18.33 ± 0.12 |
| llama 70B Q5_K - Medium        |  45.40 GiB |    68.98 B | CPU        |         64 |         tg128 |      6.73 ± 0.01 |


Its a pretty severe slowdown, so I hope this helps track it down. 
I'm only sporadically available over the next week, but please let me know if there is any testing I can do and I'll do it as soon as I'm able.
```

## What you have

- `/testbed/repo` is a git clone of `ggml-org/llama.cpp` truncated just after the regression was
  reported.  `HEAD` is `fcf6538ba6702c55eaec70da9a75c81d04900a72` and the full history behind it is present.
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
