# Locate the commit that introduced this regression

A regression was reported against `ggml-org/llama.cpp`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Regression: llama.cpp produces nonsensical outputs when using batched decoding on Metal

When using batched decoding with >1 parallel sequences, llama.cpp produces nonsensical outputs. Here is an example:
```
MacintoBookPro3:llama.cpp Ari🍉  ./batched openhermes-2.5-mistral-7b.Q4_0.gguf "<|im_start|>user\nWhat is 20+20?<|im_end|>\n<|im_start|>assistant\n20+20=" 2 110 80
[...]
main: generating 2 sequences ...

main: stream 0 finished at n_cur = 110
main: stream 1 finished at n_cur = 110

sequence 0:

<|im_start|>user\nWhat is 20+20?<|im_end|>\n<|im_start|>assistant\n20+20=2+2020202+2<|/im_end|>2<|<|

## 2+20+202022|0202020202202020202020202

sequence 1:

<|im_start|>user\nWhat is 20+20?<|im_end|>\n<|im_start|>assistant\n20+20=0\n<|im assistant|> 
02+02+2+20+2+20+20+20+2+20+2+0+2+2+02020+202+2+2+2+2+
```

However, if I use only 1 parallel sequence instead of 2, the output becomes reasonable:
```
MacintoBookPro3:llama.cpp Ari🍉  ./batched openhermes-2.5-mistral-7b.Q4_0.gguf "<|im_start|>user\nWhat is 20+20?<|im_end|>\n<|im_start|>assistant\n20+20=" 1 110 80
[...]
 <|im_start|>user\nWhat is 20+20?<|im_end|>\n<|im_start|>assistant\n20+20=40<|im_end|>\n\n<|im_start|>user\nCan you explain how you got the answer?<|im_end|>\n\n<|im_start|>assistant\nSure! To find the sum of 20 and 2
```

 

```
MacintoBookPro3:llama.cpp Ari🍉  ./batched openhermes-2.5-mistral-7b.Q4_0.gguf "<|im_start|>user\nWhat is 20+20?<|im_end|>\n<|im_start|>assistant\n20+20=" 2 110 80
[...]
main: generating 2 sequences ...

main: stream 0 finished at n_cur = 110
main: stream 1 finished at n_cur = 110

sequence 0:

<|im_start|>user\nWhat is 20+20?<|im_end|>\n<|im_start|>assistant\n20+20=40<|im_end|>\n\n<|im_start|>user\nWhat is 20-20?<|im_end|>\n<|im_start|>assistant\n20-20=0<|im_end|>\n

sequence 1:

<|im_start|>user\nWhat is 20+20?<|im_end|>\n<|im_start|>assistant\n20+20=40<|im_end|>\n<|im_start|>user\nWhat is 20*20?<|im_end|>\n<|im_start|>assistant\n20*20=400<|im_end|>\n
```



Notes:
* I am testing using Metal on a MacBook Pro with M2 Max
* Using OpenHermes 2.5 (Mistral) model at Q4_0 quantization, however the problem occurs with other quants too (tested Q8_0)


Thank you for all of the wonderful work going into this project!
```

## What you have

- `/testbed/repo` is a git clone of `ggml-org/llama.cpp` truncated just after the regression was
  reported.  `HEAD` is `bd60d82d0cc8b6852ec535495a5042dbdf05de24` and the full history behind it is present.
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
