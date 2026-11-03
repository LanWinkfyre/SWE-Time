# Locate the commit that introduced this regression

A regression was reported against `llvm/llvm-project`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
The test tries to exercise various intrinsics and compares the result generate to an expected result. After the mentioned change, the value produced is no longer the value that is expected. The repro is a little large, but should show the issue.
```c++
extern "C" {
void printf(...);
void sprintf(...);
}
typedef unsigned __v4su __attribute__((__vector_size__(16)));
typedef long __m128i __attribute__((__vector_size__(16)));
__m128i _mm_max_epu32(__m128i __V1, __m128i __V2) {
  return __builtin_elementwise_max((__v4su)__V1, (__v4su)__V2);
}
typedef long __m256i __attribute__((__vector_size__(32)));
template <typename T> T zero_upper(T in, unsigned) { return in; }
void init(char pred, void *data, unsigned size) {
  unsigned char *bytes = (unsigned char *)data;
  for (unsigned i = 0; i != size; ++i)
    bytes[i] = pred + i;
}
char print_tmp[1];
void print(char *msg, void *data, unsigned size) {
  unsigned char *bytes = (unsigned char *)data;
  for (unsigned i = 0; i != size; ++i)
    sprintf(print_tmp + i * 2, "%02x", bytes[size - 1 - i]);
  printf("%s:%s\n", msg, print_tmp);
}
__m256i test17___trans_tmp_8;
__m128i test17___trans_tmp_7, test17___trans_tmp_6, test17___trans_tmp_5,
    test17___trans_tmp_4, test17_id3723, test17_id3728, test17_id3733,
    test17_id3736, test17_id3739, test17_id3741, test17_id3742, test17_id3744,
    test17_id3746;
void test17() {
  init(139, &test17_id3723, sizeof(test17_id3723));
  __m128i id3720 = _mm_max_epu32(test17_id3723, test17_id3728), id3731;
  init(240, &id3731, sizeof(id3731));
  __m128i descriptor = id3731;
  unsigned index(id3731[0]);
  if (index > 4 || id3731[0] && index)
    descriptor &= 8;
  test17___trans_tmp_4 = __builtin_ia32_extrq(id3720, descriptor);
  init(13, &test17_id3733, sizeof(test17_id3733));
  for (char id3734_idx = 0; id3734_idx < 78; ++id3734_idx) {
    init(16, &test17_id3736, sizeof(test17_id3736));
    init(80, &test17_id3739, sizeof(test17_id3739));
    for (char id3740_idx = 0; id3740_idx < 122; ++id3740_idx) {
      init(17, &test17_id3741, sizeof(test17_id3741));
      test17_id3739 -= test17_id3741;
    }
    init(119, &test17_id3742, sizeof(test17_id3742));
    for (char id3743_idx = 0; id3743_idx < id3734_idx; ++id3743_idx) {
      init(8, &test17_id3744, sizeof(test17_id3744));
      test17_id3742 *= test17_id3744;
    }
    test17___trans_tmp_5 =
        __builtin_ia32_pshufb128(test17_id3739, test17_id3742);
    init(192, &test17_id3746, sizeof(test17_id3746));
    test17___trans_tmp_6 =
        __builtin_ia32_pmaddwd128(test17___trans_tmp_5, test17_id3746);
    test17___trans_tmp_7 =
        __builtin_ia32_pavgb128(test17_id3736, test17___trans_tmp_6);
    test17_id3733 += test17___trans_tmp_7;
  }
  int id3732(__builtin_ia32_vec_ext_v8hi(test17_id3733, 0));
  __m128i id3718(__builtin_ia32_vec_set_v8hi(test17___trans_tmp_4, id3732, 4));
  test17___trans_tmp_8 = __builtin_shufflevector(id3718, id3718, 0, 1, 1, 1);
  __m256i id3717(zero_upper(test17___trans_tmp_8, 8));
  long id3716(__builtin_ia32_vec_ext_v4di(id3717, 1));
  print("", &id3716, sizeof(id3716));
}
int main() { test17(); }
```
Compile with `clang++ -O2 -march=btver2 repro.cpp -o test.elf`. And then run the produced binary and inspect the output that it generates.
```console
$ ./test.good.elf
:0000000000009c04
$ ./test.bad.elf
:9a99989796959c04
```
```

## What you have

- `/testbed/repo` is a git clone of `llvm/llvm-project` truncated just after the regression was
  reported.  `HEAD` is `36f325413ec27819f8e4c1cd22d5f5e8a6a43000` and the full history behind it is present.
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
